import os;
import json;
from libs.GapsCleaner import GapCleaner;
from libs.MLimageConverter import ImageConverter;
from PIL import Image, ImageOps, ImageDraw, ImageFont;
import libs.KernelLib

class Font:
    def __init__(self):
        self.font= None;
        self.fonturl= None;
        self.isok= True
class Dataholder:
    def __init__(self):
        self.FontPath= '/System/Library/Fonts';
        self.image_size= (28, 28);
        self.letter_image_size= (40, 40);
        self.exclude_lst= [
            "LastResort.otf", "NotoSerifMyanmar.ttc", "ZapfDingbats.ttf", 
            "Apple Braille.ttf", "Apple Braille Outline 6 Dot.ttf", 
            "Apple Braille Pinpoint 6 Dot.ttf", "NotoSansMyanmar.ttc", 
            "GeezaPro.ttc", "SFArabic.ttf",  "NotoSansArmenian.ttc", 
            "Apple Braille Pinpoint 8 Dot.ttf", "Apple Braille Outline 8 Dot.ttf", 
            "Symbol.ttf", "NotoSansOriya.ttc", "KohinoorGujarati.ttc",
            "NotoNastaliq.ttc", "NotoSansKannada.ttc", "ArialHB.ttc",
            "NewYork.ttf", "NewYorkItalic.ttf", "Keyboard.ttf"
        ];
        self.letters_lst= [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numbers_lst= ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.symbols_lst= ['+', '-', '*', '/', '(', ')', '%', '#', '$']
        self.fonts= self.__GetFonts();
    def __GetFonts(self):
        fonts= []
        for font in os.listdir(self.FontPath):
            if font not in self.exclude_lst:
                if "NewYork" in font:
                    print(font)
                fmod= Font();
                fmod.font= font;
                fmod.fonturl= f'{self.FontPath}/{font}';
                fonts.append(fmod);
        return fonts;
class PathHolder:
    def __init__(self, name= None, extra= None):
        self.__root= 'datasets';
        self.train= f'{self.__root}/train';
        self.eval= f'{self.__root}/eval';
        self.imgpath= f'images/chars/{name if not extra else name+"-"+extra}';

        for path in [self.__root, self.train, self.eval, self.imgpath]:
            if not os.path.isdir(path):
                os.system(f'mkdir -p {path}');
        self.train+= f'/{name if not extra else name+"-"+extra}.json';
        self.eval+= f'/{name if not extra else name+"-"+extra}.json';

class CharBuilder:
    def __init__(self):
        self.buildedChars= [];
        self.__dholder= Dataholder();
        self.__degrees= None;
        self.__save_counter= 0;
        self.__error_counter= 0;
    
    def __Switcher(self, type, extra):
        holder= None;
        if(type== "small_letters"):
            holder= PathHolder(name= type, extra= extra);
            holder.fonts= [x for x in self.__dholder.fonts];
            holder.chars= [x.lower() for x in self.__dholder.letters_lst];
            return holder;
        elif(type== "big_letters"):
            holder= PathHolder(name= type, extra= extra);
            holder.fonts= [x for x in self.__dholder.fonts];
            holder.chars= [x.upper() for x in self.__dholder.letters_lst];
            return holder;
        elif(type== "numbers"):
            holder= PathHolder(name= type, extra= extra);
            holder.fonts= [x for x in self.__dholder.fonts];
            holder.chars= [x.upper() for x in self.__dholder.numbers_lst];
            return holder;
        elif(type== "symbols"):
            holder= PathHolder(name= type, extra= extra);
            holder.fonts= [x for x in self.__dholder.fonts];
            holder.chars= [x for x in self.__dholder.symbols_lst];
            return holder;
        else:
            print("Selection not Included.");
            print("Selections: [small_letters, big_letters, numbers, symbols].");
    def __BuildChar(self, font= None, char= None, size= None, degrees= None):
        self.__blank= Image.new("RGB", size, (0,0,0));
        self.__draw= ImageDraw.Draw(self.__blank);
        self.__font= ImageFont.truetype( font= font.fonturl, size= round((sum(size)//2)* .7) )
        self.__draw.text((2,0), text= str(char), fill= "white", font= self.__font);
        return ImageOps.grayscale(self.__blank);
    def __SaveCropped(self, cropped_images= None, char= None, font= None, perc= None, holder= None):
        for cropped in cropped_images:
            self.__save_counter+= 1;
            imgfull= f'{char}-{str(perc).replace(".","")}{self.__save_counter}-{font.font.replace(".","").replace(" ","")}.png';
            cropped.save(f'{holder.imgpath}/{imgfull}');
    def __CharGenerator(self, holder= None, minmax= None, letter_size= None, train_size= None):
        for fid, font in enumerate(holder.fonts):
            for cid, char in enumerate(holder.chars):
                for size in range(max(minmax), min(minmax), -1):
                    small_perc= size/10;
                    try:
                        raw_char= self.__BuildChar(font= font, char= char, size= letter_size);
                        cropped= GapCleaner(image= raw_char, size= train_size, smallperc= small_perc, degrees= self.__degrees);
                        self.__SaveCropped(
                            cropped_images= cropped.images, 
                            char= char, perc= small_perc, 
                            font= font, holder= holder);
                        images= [ImageConverter(pillowimage= image, label= char, font=font)
                            for image in cropped.images];
                        [self.buildedChars.append(image) for image in images];
                        print(f'[{fid} : {self.__error_counter} /{len(holder.fonts)}] [{small_perc}] [{char} : {font.font.replace(" ","")}]');
                    except:
                        self.__error_counter+= 1;
                print("------------");
        return True;

    def __SaveData(self, holder= None, extra= None):
        try:
            with open(holder.train, "w") as file:
                file.write(json.dumps([x.__dict__ for x in self.buildedChars], indent= 4));
        except:
            print("[ERROR]: Save could not be complete.")
    def BuildChars(self, type= None, extra= None, minmax= (), letter_size= (60,60), train_size= (28,28), degrees= None):
        if(type and minmax):
            self.__degrees= degrees;
            holder= self.__Switcher(type, extra);
            if self.__CharGenerator(holder= holder, minmax= minmax, letter_size= letter_size, train_size= train_size):
                self.__SaveData(holder= holder);
        else:
            print("[MISSING]: [type or minmax] not defined.")

cb= CharBuilder()
cb.BuildChars(type= "numbers", extra="50x50", minmax= (9, 3), train_size= (50,50));
