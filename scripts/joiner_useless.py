text1 = 'पन्नग,अहि,विषधर,लेलिहान,भुजङ्गम,नाग,उरग,फणिन्,सर्प'
text2 = 'वैरिन्,आराति,अमित्र,अरि,द्विष्,सपत्न,द्विषत्,रिपु,भ्रातृव्य,दुर्जन,शत्रु,दुष्ट,द्वेषिन्,खल,अहित'
lst1 = text1.split(',')
lst2 = text2.split(',')
result = []
for a in lst1:
	for b in lst2:
		result.append(a + b)
print(','.join(result))
