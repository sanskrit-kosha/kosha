import codecs
import re
import json

"""
Holds different reusable utilities for other programs.
"""


def extract_tag(metaline):
	# Typical line in metadata is of the structure `;tag{value}`
	m = re.search(';([^{]*)\{([^}]*)\}', metaline)
	# If matches typical line,
	if m:
		# Extract tag and value.
		tag = m.group(1)
		value = m.group(2)
	else:
		tag = False
		value = False
	return (tag, value)

def prepare_metadata(metatext):
	"""Extract metadata from the text file and return a dict."""

	# Read line wise
	lines = metatext.split('\n')
	# Initialize the blank metadata dict.
	metadata = {}
	for line in lines:
		# Ignore if the line is blank or a marker for starting of metadata.
		if line.startswith(';METADATA') or line == '':
			pass
		# If the line does not start with ';' - there is some error.
		elif not line.startswith(';'):
			print('Check line. Does not follow metadata structure.')
			print(line)
		else:
			(tag, value) = extract_tag(line)
			if tag:
				# Add to the metadata dict.
				metadata[tag] = value
			else:
				# There may be some error. Check up.
				print('Check line. Does not follow metadata structure.')
	return metadata


def remove_page_line(content):
	"""Remove page markers and line markers."""

	result = []
	# read lines into a list
	lines = content.split('\n')
	for line in lines:
		# Ignore the page and line markers
		if line.startswith(';p{') or line.startswith(';l{'):
			pass
		else:
			# Add to the output list
			result.append(line)
	# Join with new line marker.
	return '\n'.join(result)



def code_to_dict(code):
	with codecs.open('dictcode.json', 'r', 'utf-8') as fin:
		dictdata = json.load(fin)
	return dictdata[code]
