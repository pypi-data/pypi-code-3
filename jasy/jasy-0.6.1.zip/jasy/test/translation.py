#!/usr/bin/env python3

import sys, os, unittest, logging, pkg_resources

# Extend PYTHONPATH with local 'lib' folder
jasyroot = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir, os.pardir))
sys.path.insert(0, jasyroot)

import jasy.js.parse.Parser as Parser
import jasy.js.parse.ScopeScanner as ScopeScanner
import jasy.js.output.Compressor as Compressor
import jasy.i18n.Translation as Translation


class Tests(unittest.TestCase):

    def process(self, code):
        node = Parser.parse(code)

        translation = Translation.Translation("de_DE", table={
            
            "Hello World": "Hallo Welt",
            "Short": "Kurz",
            "Thank you for the flowers": "Danke für die Blumen",
            
            "Hello %1!": "Hallo: %1!",
            "Hello %1! %1!": "Hallo: %1! %1!",
            
            "Chat (noum)": "Unterhaltung",
            "Chat (noum) %1": "Unterhaltung %1",
            
            "You have got a new mail": "Du hast eine neue E-Mail",
            "You have got new mails": "Du hast neue E-Mails",
            "You have got %1 new mails": "Du hast %1 neue E-Mail erhalten"
            
        })
        
        translation.patch(node)
        
        return Compressor.Compressor().compress(node)        


    def test_basic(self):
        self.assertEqual(self.process(
            '''
            function wrapper()
            {
                alert(this.tr("Hello World"));
                alert(tr("Short"));
                alert(core.Locale.tr("Thank you for the flowers"));
            }
            '''),
            'function wrapper(){alert("Hallo Welt");alert("Kurz");alert("Danke für die Blumen")}'
        )


    def test_vars1(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(tr("Hello %1!", "Peter"))
            }
            '''),
            'function wrapper(){alert("Hallo: "+("Peter")+"!")}'
        )        

    def test_vars2(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(tr("Hello %1! %1!", "Peter"))
            }
            '''),
            'function wrapper(){alert("Hallo: "+("Peter")+"! "+("Peter")+"!")}'
        )        

    def test_vars3(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(tr("Hello %1!", this.getGreetingName()))
            }
            '''),
            'function wrapper(){alert("Hallo: "+this.getGreetingName()+"!")}'
        )
            
    def test_vars4(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(tr("Hello %1! %1!", this.getGreetingName()))
            }
            '''),
            'function wrapper(){alert("Hallo: "+this.getGreetingName()+"! "+this.getGreetingName()+"!")}'
        )        
 
    def test_trc1(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(trc("Chat (noum)", "Chat"));
            }
            '''),
            'function wrapper(){alert("Unterhaltung")}'
        )
        
    def test_trc2(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(trc("Chat (noum) %1", "Chat %1", "Online"));
            }
            '''),
            'function wrapper(){alert("Unterhaltung "+("Online"))}'
        )
        
    def test_trc3(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(trc("Chat (noum) %1", "Chat %1", this.getChatStatus()));
            }
            '''),
            'function wrapper(){alert("Unterhaltung "+this.getChatStatus())}'
        )
        
        
    def test_trn1(self):
        self.assertEqual(self.process(
            '''
            function wrapper() {
                alert(trn("You have got a new mail", "You have got new mails", newMails));
            }
            '''),
            'function wrapper(){alert((newMails<=1?"Du hast eine neue E-Mail":"Du hast neue E-Mails"))}'
        )

    def test_trn2(self):
        self.assertEqual(self.process(
            '''
            function wrapper()
            {
                alert(trn("You have got a new mail", "You have got %1 new mails", newMails, newMails));
            }
            '''),
            'function wrapper(){alert((newMails<=1?"Du hast eine neue E-Mail":"Du hast "+newMails+" neue E-Mail erhalten"))}'
        )


    def test_marktr(self):
        self.assertEqual(self.process(
            '''
            function wrapper()
            {
                // Register strings in translation file (will be compiled out)
                // According to doc, marktr() does mark for tranlsation, but always returns the original text.
                marktr("Dog");
                marktr("Cat");
                marktr("Bird");

                // After marking the text these can be used for translation
                var objs = ["Dog","Cat","Bird"];
                for (var i=0, l=objs.length; i<l; i++) {
                    alert(tr(objs[i]));
                }
            }
            '''),
            'function wrapper(){;;;var objs=["Dog","Cat","Bird"];for(var i=0,l=objs.length;i<l;i++){alert(tr(objs[i]))}}'
        )




if __name__ == '__main__':
    logging.getLogger().setLevel(logging.ERROR)
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


