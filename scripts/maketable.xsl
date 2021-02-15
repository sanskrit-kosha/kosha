<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Verses of ekAkSaranAmamAlA</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>Headword</th>
      <th>HW Gender</th>
      <th>Meaning</th>
      <th>Meaning Gender</th>
      <th>Verse</th>
      <th>Verse Number</th>
      <th>Page Number</th>
    </tr>
    <xsl:for-each select="root/content/word/meanings/m/hw">
    <tr>
      <td><xsl:value-of select="../../../headword/hw"/></td>
      <td><xsl:value-of select="../../../headword/gender"/></td>
      <td><xsl:value-of select="."/></td>
      <td><xsl:value-of select="../gender"/></td>
      <td>
        <xsl:for-each select="../../../verse/line">
          <xsl:value-of select="."/>
          <br />
        </xsl:for-each>
      </td>
      <td><xsl:value-of select="../../../verseNumber"/></td>
      <td><xsl:value-of select="../../../pageNumber"/></td>
    </tr>
    </xsl:for-each>
  </table>

  <table>
  </table>

  </body>
  <h2>Metadata</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>tag</th>
      <th>value</th>
    </tr>
    <xsl:for-each select="root/meta">
      <xsl:for-each select="*">
        <tr>
        <td><xsl:value-of select="local-name(.)"/></td>
        <td><xsl:value-of select="."/></td>
        </tr>
      </xsl:for-each>
    </xsl:for-each>
  </table>
  </html>
</xsl:template>

</xsl:stylesheet>
