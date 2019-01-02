from wordsuggester import WordSuggester
import hfst, libhfst, re, time, translator
from tkinter import *
import tkinter.font


def loadTransducer():
    try:
        istr = libhfst.HfstInputStream(r"italian_verb_analyzer.hfst")
        transducers = []        
        while not (istr.is_eof()):
            transducers.append(istr.read())
            
        istr.close()
        td = hfst.HfstBasicTransducer(transducers[1])       
        return td  
    except:
        print('Transducer file was invalid or not found.')
        time.sleep(3)
        exit()
        

class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master,height=500,width=700,bg='snow')
        if(master):
            master.title('Italyzer')

        self.output_font = tkinter.font.Font(family="newspaper", size=12)
        myFont = tkinter.font.Font(family="fangsong ti")
        text.configure(font=myFont)

        self.pack_propagate(0)
        self.word = ""
        self.pack()
        self.createWidgets()
        self.transducer = loadTransducer()
        self.suggestions = False

        
           
    def set_output(self, elts):
        self.OUTPUT.delete(0,END)
        self.output_dict={}
        if len(elts)>0:
            for elt in elts:
                self.output_dict[str(elt)]=elt
                self.OUTPUT.insert(END,str(elt))
        else:
            self.OUTPUT.insert(0,"")

    def add_to_output(self, word):
            self.OUTPUT.insert(END,word)
            self.OUTPUT.update()

    def onselect(self, evt):
        # When a suggested word form is clicked
        w = evt.widget
        index = int(w.curselection()[0])
        if index > 2 and index < self.OUTPUT.size() and self.suggestions:
            value = w.get(index)
            self.recognize(value)
            self.TEXT.delete(0, END)
            self.TEXT.insert(0, value)
            self.TEXT.focus()
            self.suggestions = False

    def createWidgets(self):
        # Instruction text
        self.LABEL = Label(self)#, font=('Times',12, 'bold'))
        self.LABEL['text']='Enter an Italian verb form:'
        self.LABEL['fg']='black'
        self.LABEL['bg']='white'
        self.LABEL.pack(side=TOP)
        
        # Text box for user input
        self.TEXT = Entry(self, font=('Times',12, 'bold'))
        self.TEXT['width'] = 30
        self.TEXT['fg'] ='black'
        self.TEXT.pack(side=TOP)
        self.TEXT.bind("<Key>", self.key)
        self.TEXT.focus()

        # 'Clear text' button
        self.CLEAR_BUTTON = Button(self, text="Clear text", command=self.clear_text, font=('Times',12, 'bold'))
        self.CLEAR_BUTTON['bg'] = 'RosyBrown1'
        self.CLEAR_BUTTON.pack()
        

        # Output box
        output_frame = Frame(self)
        scrollx = Scrollbar(output_frame,orient=HORIZONTAL)
        scrolly = Scrollbar(output_frame)
        self.OUTPUT = Listbox(output_frame,height=15,width=65, background='white', \
                    yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, \
                    selectmode=BROWSE, font=('Times',11, 'bold'))
        self.OUTPUT['height'] = 15
        self.OUTPUT['width'] = 60
        self.OUTPUT.bind('<<ListboxSelect>>', self.onselect)
        self.OUTPUT['bg'] = 'snow'
        self.OUTPUT.pack(side=BOTTOM)
        self.OUTPUT.insert(0,"")
        output_frame.pack(side=BOTTOM)

        # 'Recognize' button
        self.RECOGNIZE = Button(self, font=('Times',12, 'bold'))
        self.RECOGNIZE['text']='Analyze'
        self.RECOGNIZE['bg']='PaleGreen1'
        self.RECOGNIZE['command']=lambda :self.press_recognize_button()
        self.RECOGNIZE['width']=15
        self.RECOGNIZE.pack(side=BOTTOM)

    def clear_text(self):
        # Clears input box
        self.TEXT.delete(0, END)
        self.TEXT.focus()

    def press_recognize_button(self):
        if self.input_is_okay(self.TEXT.get()):
            self.suggestions = False
            self.word = self.TEXT.get().lower()
            self.recognize(self.word)

    def recognize(self, word):
        if len(self.transducer.lookup(word).values()) < 1 or not wordsuggester.word_in_lexicon(word):
            self.OUTPUT.delete(0,  self.OUTPUT.size())
            self.set_output(['Verb form not found.'])
            self.add_to_output('')
            
            if len(wordsuggester.suggestions(word)) > 0 and len(word) > 2:
                self.display_suggestions(word)
        else:
            self.display_analyses(word)

    def display_suggestions(self, word):
        self.suggestions = True
        self.add_to_output('Did you mean:')
        for count, form in enumerate(wordsuggester.suggestions(word)):
            if count < 10:
                self.add_to_output(form)

    def display_analyses(self, word):
        self.OUTPUT.delete(0,  self.OUTPUT.size())
        for form_list in self.transducer.lookup(word).values():
            for form in form_list:
                analysis = form[0].replace(epsilon, '')
                analysis += '   -   ' + str(translator.translate(form[0].split('+')[1]))
                self.add_to_output(analysis)

    def key(self, event):
        # Keyboard shortcuts: 'Enter' to analyze, Right and Left control to clear input box
        if (event.keysym) == 'Return' and self.input_is_okay(self.TEXT.get()):
            self.suggestions = False
            self.recognize(self.TEXT.get().lower())
        if (event.keysym) == 'Control_L' or (event.keysym) == 'Control_R':
            self.clear_text()

    def input_is_okay(self, usinput):
        # Checks that input has only one word and contains legit characters
        if re.search("[a-zA-Zèàìòù\-\']+",self.TEXT.get()) and len(self.TEXT.get().split(' ')) == 1:
            return True
        return False


if __name__=='__main__':
    epsilon = '@_EPSILON_SYMBOL_@'
    wordsuggester = WordSuggester()
    root = Tk()
    text = Text(root)

    app = Application(master=root)
    app.mainloop()
