#!/usr/bin/env python
import json
import os, subprocess
import emoji
import re

import networkx as netx
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from tqdm import tqdm
from random import choice
from time import time
from wordcloud import WordCloud


# config
with open(os.path.abspath("../config.json"), "r", encoding="utf8") as fobj:
	CONFIG = json.load(fobj)

PATH_PREFIX = input("advanced package prefix (or press enter): ")
PATHS = {
	"PACKAGE": os.path.abspath(CONFIG["package_directory"].format(ID=PATH_PREFIX)),
	"RESULTS": os.path.abspath(CONFIG["results_directory"].format(ID=PATH_PREFIX))
}
PATHS["ACCOUNT"]  = os.path.abspath(os.path.join(PATHS["PACKAGE"], "account"))
PATHS["ACTIVITY"] = os.path.abspath(os.path.join(PATHS["PACKAGE"], "activity"))
PATHS["MESSAGES"] = os.path.abspath(os.path.join(PATHS["PACKAGE"], "messages"))
PATHS["PROGRAMS"] = os.path.abspath(os.path.join(PATHS["PACKAGE"], "programs"))
PATHS["SERVERS"]  = os.path.abspath(os.path.join(PATHS["PACKAGE"], "servers"))

DIRS = {
	"MESSAGES": os.listdir(PATHS["MESSAGES"]),
	"SERVERS":  os.listdir(PATHS["SERVERS"])
}

with open(os.path.abspath(os.path.join(PATHS["ACCOUNT"], "user.json")), encoding="utf8") as fobj: DATA_USER = json.load(fobj)
with open(os.path.abspath(os.path.join(PATHS["MESSAGES"], "index.json")), encoding="utf8") as fobj: DATA_IDS = json.load(fobj)
DATA_IDS[DATA_USER["id"]] = DATA_USER["username"]


# analysed parameters
messages = 0
message_contents = 0
message_contents_list = []
message_contents_linebreaks = 0
message_contents_emoji_unicode = 0
message_contents_emoji_custom = 0
message_attachments = 0
message_attachments_links = []
message_distinct_characters = 0
message_character_frequency = dict()
message_most_character = " "

# relationships graphs
relships_graph = netx.Graph()

# add data user as first node
relships_graph.add_nodes_from([(
	int(DATA_USER["id"]),
	{
		"name": DATA_USER["username"],
		"ctype": -1
	}
)])


# progress bar init for analyse
analyse_pbar_size = (len(DIRS["MESSAGES"]) - 1) * 11 + 4
analyse_pbar = tqdm(total=analyse_pbar_size)

# iterate all messages directories ordered by channel id
t0 = time()
for directory in DIRS["MESSAGES"]:
	
	# get files
	dir_path = os.path.join(PATHS["MESSAGES"], directory)
	if not os.path.isfile(dir_path):
		
		# local analyse parameters
		local_messages = 0
		
		# get message file
		file_path = os.path.join(dir_path, "messages.json")
		
		# open messages file
		with open(file_path, "r", encoding="utf8") as fobj:
			json_reader = json.load(fobj)
			
			# iterate messages
			for data in json_reader:
				
				# analyse messages
				messages += 1
				local_messages += 1
				
				# analyse message contents
				data_content = data['Contents']
				if data_content != "":
					message_contents += 1
					
					# add content to message list
					message_contents_list.append(data_content)
					
					# analyse content line breaks
					message_contents_linebreaks += data_content.count("\n")
					
					# analyse content unicode emojis
					message_contents_emoji_unicode += emoji.emoji_count(data_content, unique = True)
				
				# analyse message attachments
				data_attachments = data['Attachments']
				if data_attachments != "":
					message_attachments += data_attachments.count(" ") + 1
					
					# analyse attachment links
					if data_attachments.startswith("https://cdn.discordapp.com/attachments/"):
						message_attachments_links.extend(data_attachments.split(" "))
				
				# iterate characters
				for char in data_content:
					
					# analyse character frequency
					if char not in message_character_frequency:
						message_character_frequency[char] = 1
					else:
						message_character_frequency[char] += 1
		
		# update analyse progress bar
		analyse_pbar.update(7)
		
		# get channel file
		file_path = os.path.join(dir_path, "channel.json")
		
		# load channel data
		with open(file_path, encoding="utf8") as fobj:
			data_channel = json.load(fobj)
		
		# add nodes in relationships graph, if id not null
		if DATA_IDS[data_channel["id"]] != None:
			
			# direct channel
			if data_channel["type"] == 1:
				for recipient in data_channel["recipients"]:
					relships_graph.add_nodes_from([(
						int(recipient),
						{
							"name": DATA_IDS[recipient].split("with")[1:] if recipient in DATA_IDS else "",
							"ctype": data_channel["type"]
						}
					)])
			# group channel
			elif data_channel["type"] == 3:
				if "recipients" in data_channel:
					for recipient in data_channel["recipients"]:
						relships_graph.add_nodes_from([(
							int(recipient),
							{
								"name": f'{DATA_IDS[recipient][:15]}...' if recipient in DATA_IDS else "",
								"ctype": data_channel["type"]
							}
						)])
			# guild channel
			elif data_channel["type"] == 0:
				if "guild" in data_channel and "id" in data_channel["guild"]:
					relships_graph.add_nodes_from([(
					int(data_channel["guild"]["id"]),
						{
							"name": data_channel["guild"]["name"],
							"ctype": data_channel["type"]
						}
					)])
		
		# update analyse progress bar
		analyse_pbar.update(2)
		
		# add channels as edges between recipients and recipients/groups/guilds in relationships graph, if id not null
		if DATA_IDS[data_channel["id"]] != None:
			
			# direct channel
			if data_channel["type"] == 1:
				relships_graph.add_edges_from([(
					data_channel["recipients"][0],
					data_channel["recipients"][1],
					{
						"cid": int(data_channel["id"]),
						"messages": local_messages,
						"name": DATA_IDS[data_channel["id"]],
						"ctype": data_channel["type"]
					}
				)])
			# group channel
			elif data_channel["type"] == 3:
				if "recipients" in data_channel:
					for recipient in data_channel["recipients"]:
						relships_graph.add_edges_from([(
							int(recipient),
							int(data_channel["id"]),
							{
								"cid": int(data_channel["id"]),
								"messages": local_messages,
								"name": DATA_IDS[data_channel["id"]],
								"ctype": data_channel["type"]
							}
						)])
			# guild channel
			elif data_channel["type"] == 0:
				if "guild" in data_channel and "id" in data_channel["guild"]:
					relships_graph.add_edges_from([(
						int(DATA_USER["id"]),
						int(data_channel["guild"]["id"]),
						{
							"cid": int(data_channel["id"]),
							"messages": local_messages,
							"name": DATA_IDS[data_channel["id"]],
							"ctype": data_channel["type"]
						}
					)])
	
		# update analyse progress bar
		analyse_pbar.update(2)

# analyse content custom emojis
mcf = message_character_frequency
message_contents_emoji_custom = (mcf["<"] + mcf[">"]) // 2
analyse_pbar.update(1)

# analyse distinct characters
message_distinct_characters = len(message_character_frequency)
analyse_pbar.update(1)

# analyse most character of messages
mcf, mmc = message_character_frequency, message_most_character
for char in mcf:
	if mcf[char] > mcf[mmc]:
		mmc = char
message_most_character = mmc
analyse_pbar.update(1)

# save message contents
with open(os.path.join(PATHS["RESULTS"], "contents.txt"), "w+", encoding="utf8") as fobj:
	fobj.write("\n".join(message_contents_list))
analyse_pbar.update(1)

# close analyse progress bar
analyse_pbar.close()


# save analyses parameters
with open(os.path.join(PATHS["RESULTS"], "data.json"), "w+", encoding="utf8") as fobj:
	data = {
		"messages": messages,
		"message_contents": message_contents,
		"message_contents_emoji_unicode": message_contents_emoji_unicode,
		"message_contents_emoji_custom": message_contents_emoji_custom,
		"message_contents_linebreaks": message_contents_linebreaks,
		"message_attachments": message_attachments,
		"message_attachments_links": message_attachments_links,
		"message_distinct_characters": message_distinct_characters,
		"message_character_frequency": message_character_frequency,
	}
	fobj.write(json.dumps(data))


# wordcloud configs
wordcloud_configs = [
	{
		"mask": "../img/discord_logo.png",
		"max_words": 5_000,
		"contour_width": 5
	},
	{
		"mask": "../img/discord_logo.png",
		"max_words": 100,
		"contour_width": 5
	},
]

# progress bar init for wordcloud
wordcloud_pbar_size = 2 + len(wordcloud_configs) * 2
wordcloud_pbar = tqdm(total=wordcloud_pbar_size)
wordcloud_pbar.update(1)

# create wordclouds
wordcloud_words = open(os.path.join(PATHS["RESULTS"], "contents.txt"), "r", encoding="utf8").read().lower()
wordcloud_pbar.update(1)

# create from different wordclouds from configs
for i, config in enumerate(wordcloud_configs):
	
	# generate wordcloud
	wordcloud_mask = np.array(Image.open(os.path.abspath(config["mask"])))
	wordcloud_cloud = WordCloud(
		background_color = "white",
		max_words = config["max_words"],
		mask = wordcloud_mask,
		contour_width = config["contour_width"],
		stopwords = set()
	)
	wordcloud_cloud.generate(wordcloud_words)
	wordcloud_pbar.update(1)
	
	# save wordcloud
	wordcloud_cloud.to_file(os.path.join(PATHS["RESULTS"], f"wordcloud_{i}_{config['max_words']}.png"))
	wordcloud_pbar.update(1)

# close wordcloud progress bar
wordcloud_pbar.close()


# progress bar init for script file generator
script_pbar_size = 3 + len(message_attachments_links) * 2
script_pbar = tqdm(total=script_pbar_size)

# create download script for all attachments
script = os.path.join(PATHS["RESULTS"], "download.py")
with open(script, "w+") as fobj:
	os.chmod(script, 0o755)
	fobj.writelines("#!/usr/bin/env python\n")
	fobj.writelines("import shutil\n")
	fobj.writelines("import os\n")
	fobj.writelines("import urllib.request\n\n")
	script_pbar.update(1)

	categories = ["unknowns", "audios", "docs", "imgs", "codes", "data", "exes", "vids", "zips"]

	# clear directories for batch download
	for category in categories:
		fobj.writelines("try: shutil.rmtree(\"{}\")\nexcept FileNotFoundError: pass\n".format(os.path.abspath(os.path.join(PATHS["RESULTS"], category))))
	script_pbar.update(1)
	
	# create directories for batch download
	for category in categories:
		fobj.writelines("os.makedirs(\"{}\")\n".format(os.path.abspath(os.path.join(PATHS["RESULTS"], category))))
	script_pbar.update(1)
	
	# setup progress bar
	scale = (len(message_attachments_links) - 1) // 100
	
	# iterate attachments
	for i, url in enumerate(message_attachments_links):
		
		# select category
		url_lower = url.lower()
		category = "unknowns"
		if re.search(r".*\.(mp3|wav|m4a).*", url_lower):
			category = "audios"
		elif re.search(r".*\.(doc(x)?|pdf).*", url_lower):
			category = "docs"
		elif re.search(r".*\.(jp(e)?g|png|gif|ico|svg).*", url_lower):
			category = "imgs"
		elif re.search(r".*\.(txt).*", url_lower):
			category = "txts"
		elif re.search(r".*\.(py(w|proj)?|htm(l)?|css|vb(a|s)?|bat|cmd|(x|y)ml|sln|vpj).*", url_lower):
			category = "codes"
		elif re.search(r".*\.(json|csv).*", url_lower):
			category = "data"
		elif re.search(r".*\.(exe).*", url_lower):
			category = "exes"
		elif re.search(r".*\.(mp4|mov).*", url_lower):
			category = "vids"
		elif re.search(r".*\.(zip|7z|tar|rar|gz).*", url_lower):
			category = "zips"
		script_pbar.update(1)
		
		# write to script file
		output_path = os.path.abspath(os.path.join(PATHS["RESULTS"], f'{category}/attachment_{i}_{category}.{url.split(".")[-1]}'))
		fobj.writelines(f"print(\"attachment_{i}_{category}: {min(i/scale, 100):.2f}%% {(i//scale)*'#'}\")\n")
		# 403 with Python-urllib/3.13 user agent
		fobj.writelines(f"with open('{output_path}', \"wb\") as file: file.write(urllib.request.urlopen(urllib.request.Request('{url}', headers={{\"User-Agent\": \"\"}})).read())\n")
		script_pbar.update(1)

# close script generator progress bar
script_pbar.close()

# ask to download now
download_now = False
download_now = bool(re.search(r"[YyJj]", input("download all attachments now (Y/N)?")))

# start script download
if download_now: download_script_return = subprocess.run([os.path.join(PATHS["RESULTS"], "download.py")])


# print character frequency
mcf, mmc = message_character_frequency, message_most_character
sorted_characters = dict(sorted(mcf.items(), key=lambda x: x[1]))
scale = mcf[mmc] // 100
for char in sorted_characters:
	
	# display graph
	displayed_char = char.replace("\n", r"\n")
	print(f"{displayed_char:<2} {mcf[char]:6d} {(mcf[char] // scale) * '='}>")

# print analysed parameters
print(f"\n{messages=}")
print(f"{message_contents=}")
print(f"{message_contents_emoji_unicode=}")
print(f"{message_contents_emoji_custom=}")
print(f"{message_contents_linebreaks=}")
print(f"{message_attachments=}")
print(f"message_attachments_links={str([ choice(message_attachments_links) for _ in range(10) ])[:-1]}, ...]")
print(f"{message_distinct_characters=}")
print(f"{message_character_frequency=}")


# set name and ctype for every node
i = 0
for node in relships_graph.nodes:
	if "name" not in relships_graph.nodes[node]: relships_graph.nodes[node]["name"] = f'{DATA_IDS[str(node)][:15]}...' if str(node) in DATA_IDS else ""
	if "ctype" not in relships_graph.nodes[node]: relships_graph.nodes[node]["ctype"] = -1
	i += 1

# node positions
# positions = netx.random_layout(relships_graph)
# positions = netx.circular_layout(relships_graph)
# positions = netx.spiral_layout(relships_graph)
positions = netx.kamada_kawai_layout(relships_graph)

# graph layout
node_labels = { node: relships_graph.nodes[node]["name"] for node in relships_graph.nodes }
node_sizes = [ sum(relships_graph.edges[edge]["messages"] for edge in relships_graph.edges(node))/10 for node in relships_graph.nodes ]
node_colors = [ ["red", "green", "black", "orange", "blue"][relships_graph.nodes[node]["ctype"]] for node in relships_graph.nodes ]
edge_colors = [ ["red", "green", "black", "orange", "blue"][relships_graph.edges[edge]["ctype"]] for edge in relships_graph.edges ]

# setup relationships graph
print(f"\n{relships_graph}")
plt.figure(figsize=(15, 10))
plt.title("Relationships between recipients and guilds via channels", size=15)
netx.draw_networkx(
	relships_graph,
	alpha = 0.6,
	pos = positions,
	labels = node_labels,
	node_size = node_sizes,
	node_color = node_colors,
	edge_color = edge_colors
)


#debug
t1 = time()
dt = t1 - t0
print(f"\n{0 if (dt//60)<10 else ''}{int(dt//60)}:{0 if (dt%60) < 10 else ''}{int(dt%60)}.{int((dt%1)*100)} minutes processing time")

# plot and relationships graph
plt.savefig(os.path.join(PATHS["RESULTS"], "relationships_graph.png"))
# plt.show()
