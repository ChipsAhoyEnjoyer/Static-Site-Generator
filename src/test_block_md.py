import unittest

from block_md import markdown_to_blocks, block_to_block_type, raw_md_to_text, markdown_to_html_node

class TestBlockMD(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(["* This is the first list item in a list block",
                           "* This is a list item",
                           "* This is another list item"],
                           blocks)
        
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading\n   
                      \n
                      This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n
                      \n
                      * This is the first list item in a list block\n
                      * This is a list item\n
                      * This is another list item"""    
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(["# This is a heading",
                          "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                          "* This is the first list item in a list block",
                          "* This is a list item",
                          "* This is another list item",],
                          blocks)
    
    def test_block_to_blocktype(self):
        h3 = "### heading3"
        self.assertEqual(block_to_block_type(h3), "h3")
        heading_error = "###heading3"
        self.assertEqual(block_to_block_type(heading_error), "p")

        code = "```print(hello world)```"
        self.assertEqual(block_to_block_type(code), "code")
        code_error = "``print('error')```"
        self.assertEqual(block_to_block_type(code_error), "p")

        blockquote = ">lorum ipsum"
        self.assertEqual(block_to_block_type(blockquote), "blockquote")

        ol = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(ol), "ol")
        ol_error = "1. one\n1. two\n1. three"
        self.assertEqual(block_to_block_type(ol_error), "p")
        ul = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(ul), "ul")
        ul_error = "- one\n-two\n-three"
        self.assertEqual(block_to_block_type(ul_error), "p")
        
        p = "paragraph"
        self.assertEqual(block_to_block_type(p), "p")

    def test_raw_md_to_text(self):
        h3 = "### heading3"
        self.assertEqual(raw_md_to_text(h3), "heading3")
        heading_error = "###heading3"
        self.assertEqual(raw_md_to_text(heading_error), "###heading3")

        code = "```print(hello world)```"
        self.assertEqual(raw_md_to_text(code), "print(hello world)")
        code_error = "``print('error')```"
        self.assertEqual(raw_md_to_text(code_error), "``print('error')```")

        blockquote = ">lorum ipsum"
        self.assertEqual(raw_md_to_text(blockquote), "lorum ipsum")

        # ol = "1. one\n2. two\n3. three"
        # self.assertEqual(raw_md_to_text(ol), "1. one\n2. two\n3. three")
        ol_error = "1. one\n1. two\n1. three"
        self.assertEqual(raw_md_to_text(ol_error), "1. one\n1. two\n1. three")
        ul = "- one\n- two\n- three"
        self.assertEqual(raw_md_to_text(ul), "one\ntwo\nthree")
        ul_error = "- one\n-two\n-three"
        self.assertEqual(raw_md_to_text(ul_error), "- one\n-two\n-three")
        
        p = "paragraph"
        self.assertEqual(raw_md_to_text(p), "paragraph")

    def test_markdown_to_html_node(self):
        text = """
# In modo
\n
\n
## Venulus de adde bracchia
\n
\n
Lorem markdownum et **possunt** hora norint et ponit recepit pleni; aere vera mihi veretur Ossae cunctantem mihi; in? Prora tinctas, grege esse *animos pugnant*: tenens Polyxena tigridis erit, fraude visi **pars aurum** ferre, mensae. [Ditissimus](http://virus.org/) sinus iugo prodest redolent puppimque corripiunt *manibus murmure ab* huc in fida luctus?
\n
\n
1. At timidum superos sollicito o victoris silva\n2. Iussitque inde nec quem cortice\n3. Mea haec magnis\n4. Nulla ad magnae demisere deosque velum quoque\n5. Solibus et ille reverentia carina morte\n6. Trepidoque corpus et tabellis curat venenis austri\n
\n
\n
[Resoluta subitarum](http://libet-genitor.net/hospitium) auro turbavit Taenarides mirarique maior, luctuque vacca, [at Est](http://agrestibusverba.net/sinit-manum) e stridula faciem. Manu genitorque sinu. Hac *iungere*: leges deus atque, tenebrasque auras Veneris quem; **licet** concavat, per quod frontem. Eluserat visa comes, trames, vocato tamen. Mihi tela, illo [potuere morbis crimine](http://pelagiest.org/eratnec) dolentem, [et](http://imbres.net/), quinque.
\n
\n
## Extrema iacentes sagitta dictas domo comites dixit
\n
\n
Palmas oscula Dardanidas regia. Animam illi manibus [poterant](http://illa.net/) caret **deus**, modo frena despexitque. Quaeri comis pars humano lupus, illinc, et et huius. Ungues loca longum volenti et templo, e *increvisse*, aut fugato: acta.
\n
Procellamnos duris quos **rabieque** moriens stare clamabat iuvenis, [visa](http://radice-temone.org/) nec quicquam **tantos**. Et cultu Hymenaee canos qui Farfarus, **iura odore** luget, cur. Falsi occidit vulgus tribuitque te repulsa mundo flores: hastam pars.
\n
\n
```
if (suffixStation * 2 + 2 - ccdMegahertzMethod.google(fontTerahertz, cadTag, restore)) {
    debugger.computer(-4);
    pupNavigationWins(26, device(facebookRatePlain, 4, timeEbookProgram), hdvClick(44, ppi, mainframe_icann));
    scsiThunderbolt = white * bar;
}
plainMultitasking += activex;
var impact = memory;
var dialog_smtp_node = bing_bar_nat + filePlatformBarcraft * ajaxMicrocomputer;
if (antivirusOn) {
    t_ram_impression = dvdStation.pc.ipv(permalink, hardOpticTablet, lion_design_unc);
    hypermedia_trash_jumper.igpAppletSearch = multimediaMegabyte;
    heuristicCardDot *= bareWeb(interlaced, componentWorkstation) + language_reader_lun;
}
```
\n
\n
- Grandaevus retexuit dedit navem magnorum\n- Postera inque\n- Dumque iuventam tinguit oculos fata pro moveri\n- Essem longique imitator misit\n- Contorto cani dei interit decor illo est\n- Clamantia videres meas frater tamen hanc Erectheas
        """
        # with open(r"./src/test_index.html", "w") as f:
        #     f.write(markdown_to_html_node(text).to_html())

