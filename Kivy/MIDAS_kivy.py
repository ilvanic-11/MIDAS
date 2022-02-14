import copy

from Kivy.midas_scripts import midiart, midiart3D, music21funcs
import cv2
import numpy as np
import shutil
import os
from importlib import reload

import sys
#sys.path
#sys.path.append(r"C:\Users\Isaac's\PycharmProjects\musicode\Kivy-20190225T023432Z-001\Kivy")
import MIDAS_Settings
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.splitter import Splitter


from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.factory import Factory
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from Kivy import musicode


balls = Splitter()
#balls3 = SplitterStrip()
balls2 = balls.strip_cls


class HeightPopup(Popup):
    note_HeightSlider = ObjectProperty(None)
    app = App.get_running_app()
    callingWidget = None

    def __init__(self, my_widget, **kwargs):  # my_widget is now the object where popup was called from.
        super(HeightPopup, self).__init__(**kwargs)

        #self.note_HeightSlider = ObjectProperty(None)
        #self.app = App.get_running_app()

    def HeightPopupDone(self):
        #super(HeightPopup,self).note_Height = self.note_HeightSlider.value
        MIDAS_Settings.noteHeight = self.note_HeightSlider.value
        print("slider value " + str(self.note_HeightSlider.value))
        self.dismiss()
    pass



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)



class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)



class MusicodeArea(BoxLayout):
    txt_Input = ObjectProperty(None)
    musicodes_sh = sorted(musicode.g.mc.shorthand)
    

    def translate_txt(self):
        # error check the txt_Input and the selected musicode
        if (self.txt_Input.text == "" or self.txt_Input == None):
            print("It's broked!!!")
            pass
        if (self.musicode_Choice.text == '  Select \n\nA Musicode'):
            Popup(title='Error',
                  content=Label(text="Choose a Musicode first."),
                  auto_dismiss=True,
                  size_hint=(0.5,0.2)
                  ).open()

        else:
            stream = musicode.g.mc.translate(self.musicode_Choice.text, self.txt_Input.text)
            stream.show('txt')


            #Strings - working path
            #file_path_img = MIDAS_Settings.filepath + os.sep + "pixels_from_midi.png"  #str
            file_path_img = MIDAS_Settings.filepath + os.sep + "pixels_from_midi_with_piano.png"

            #musicode_default_img = MIDAS_Settings.musicode_default

            #Remove existing, if true
            if os.path.exists(file_path_img) is True:  # Catch for fileexists error. Remove and rewrite, since will be commonly called.
                shutil.rmtree(file_path_img, ignore_errors=True)
            # if os.path.exists(
            #         file_path_img) is True:  # Catch for fileexists error. Remove and rewrite, since will be commonly called.
            #     shutil.rmtree(file_path_img, ignore_errors=True)

            #Pixels from Midi
            #display_image = music21funcs.chop_up_notes(stream, 0.5)
            q = midiart.make_pixels_from_midi(stream,   #display_image,
                                              color= (255., 255. , 255.), #bgr #R n B are swapped here.. just fyi
                                              background_color=(88.,88.,88.),
                                              gran=32) #png  #
            #cv2.error: OpenCV(3.4.4) C:\projects\opencv-python\opencv\modules\imgproc\src\resize.cpp:3662: error:
            # (-215:Assertion failed) func != 0 in function 'cv::hal::resize'



            cv2.imwrite(file_path_img, q) #png written to file.

            #Midi to file
            filepath_midi = MIDAS_Settings.filepath + os.sep + "musicode_write.mid"
            if os.path.exists(filepath_midi) is True:  # Catch for fileexists error. Remove and rewrite, since will be commonly called.
                shutil.rmtree(filepath_midi, ignore_errors=True)

            stream.write("mid", filepath_midi)                                             #midi written to file.

            #Image with piano
            img_with_piano = self.parent.ids.musicodedraw_Area.join_with_piano(q)
            # print("IMG_WITH_PIANO_dtype", img_with_piano.dtype)
            # print("IMG_WITH_PIANO", img_with_piano)
            # print("IMG_WITH_PIANO_TYPE", type(img_with_piano))
            # img_with_piano = np.array(img_with_piano, dtype=np.uint8)

            ###
            ###Double the height via a resize; for better, more visible display
            img_with_piano = cv2.resize(img_with_piano, (img_with_piano.shape[1], len(img_with_piano) * 2))
            ###

            #Image with piano to file
            cv2.imwrite(file_path_img, img_with_piano)

            #Force a change, by going to default image first....
            #self.parent.ids.musicodedraw_Area.ids.musicode_View.source = musicode_default_img
            #...and then to our desired one.
            self.parent.ids.musicodedraw_Area.ids.musicode_View.source = file_path_img
            self.parent.ids.musicodedraw_Area.ids.musicode_View.reload()

            print(self.txt_Input.text)




class MidiArtButtons(BoxLayout):
    note_Height = StringProperty()
    txtKey = ObjectProperty()
    granularities = ["32nd Note","16th Note","8th Note","Quarter Note","Half Note","Whole Note"]
    granularities_num = [.125, .25, .5, 1, 2, 4]
    granularities_dict = dict(zip(granularities, granularities_num))
    current_color_palette = MIDAS_Settings.current_color_palette


    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)


    def __init__(self,**kwargs):
        super(MidiArtButtons, self).__init__(**kwargs)
        self.heightPopup = HeightPopup(self)
        self.note_Height = str(MIDAS_Settings.noteHeight)
        self.granularity = str(MIDAS_Settings.granularity)
        self.heightPopup.bind(on_dismiss = self.updateHeightLabel)


    def updateHeightLabel(self,instance):
        self.note_Height = str(MIDAS_Settings.noteHeight)
        print("Note height changed to: ", str(MIDAS_Settings.noteHeight))


    def updateGranularity(self):
        MIDAS_Settings.granularity = self.granularity_Choice.text

        print("Granularity changed to: ", str(MIDAS_Settings.granularity))


    def updateConnectNotes(self):
        if (self.ids.tb_Y.state == "down"):
            MIDAS_Settings.connectNotes = True
            print("ConnectNotes changed to: True")
        elif(self.ids.tb_N.state == "down"):
            MIDAS_Settings.connectNotes = False
            print("ConnectNotes changed to: False")


    def updateKey(self):
        MIDAS_Settings.key = self.ids.txt_Key.text
        #"A A#m Ab Abm Am B Bb Bbm Bm C C# C#m Cb Cm D D#m Db Dm E Eb Ebm Em F F# F#m Fm G G#m Gb Gm"
        print("Key updated to:", MIDAS_Settings.key)


    def updateColor(self):
        MIDAS_Settings.color = self.ids.colors_Choice.text
        if MIDAS_Settings.color == 'Select Color':
            pass
        else:
            MIDAS_Settings.current_color_palette = MIDAS_Settings.clr_dict_list[MIDAS_Settings.color]
        print("Color updated to:", MIDAS_Settings.color)


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        try:
            MIDAS_Settings.image = os.path.join(path, filename[0])



        #/musicode/Kivy/MIDAS_kivy.py", line 138, in load
        #MIDAS_Settings.image = os.path.join(path, filename[0])
        #IndexError: list index out of range
        except IndexError as i:
            print("INDEX ERRRROROROR", i)
            pass
        self.dismiss_popup()
        print("Loaded: -->", MIDAS_Settings.image)

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


    def dismiss_popup(self):
        print("Image File Name: ", MIDAS_Settings.image)  #was self.imageFile
        #print("self.ids", self.ids)
        #print("self.ids.image_View", self.ids.image_View)
        #MidiDrawArea.source = MIDAS_Settings.image
        #MidiDrawArea.source = StringProperty(MIDAS_Settings.image)
        #self.ids["image_View"].source = MIDAS_Settings.image
        #self.parent.midi_draw_area.ids["image_View"].source = MIDAS_Settings.image
        #MidiDrawArea()
        self.parent.ids.imagedraw_Area.change_image(MIDAS_Settings.image)

        self.parent.refresh_counter = 0
        if self.parent.refresh_counter == 0:
            self.parent.ids.imagedraw_Area.ids.image_View.keep_ratio = True
        else:
            pass

        #self.ids.image_View.source = MIDAS_Settings.image
        #self.parent.midi_draw_area.source = MIDAS_Settings.image
        #Image(source=MIDAS_Settings.image)
        self._popup.dismiss()
        #self.parent.ids.midi_draw_area.ids.image_View.reload()
        print("SUPER!")


    def transform_image(self, image=MIDAS_Settings.image):

        if not self.ids.midiart_Choice.text.isupper():   #***Here.
            #height = int(self.sldrHeight.GetValue())

            pathname = image
            print("MIDAS_Settings.image", MIDAS_Settings.image)
            print("PATHNAME", pathname)

            #self.pathname = pathname
            self.img = cv2.imread(pathname, 0)  # 2D array (2D of only on\off values.)
            self.img2 = cv2.imread(pathname, cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)

            height = MIDAS_Settings.noteHeight
            width = int(height / len(self.img) * len(self.img[0]))

            # print(type(self.img))
            img_name = os.path.basename(pathname).partition('.png')[0]
            print("IMG_NAME", img_name)

            resizedImg = cv2.resize(self.img, (width, height), cv2.INTER_AREA)
            resizedImg2 = cv2.resize(self.img2, (width, height), cv2.INTER_AREA)
            pixels = resizedImg     #2D array (2D of only on\off values.)
            pixels2 = resizedImg2   #3D array (2D of color tuples)

            #Test -This was the magical one that found our bug. 11/30/2021
            #pixels2 = cv2.cvtColor(pixels2, cv2.COLOR_BGR2RGB)

            #pixels_resized = dialog.resizedImg

            gran = self.granularities_dict[MIDAS_Settings.granularity]

            # print("PIXELS", pixels)
            # print("PIXELS2", pixels2)
            # print("PIXELS_RESIZED:", pixels, type(pixels))
            # print("pixel s_shape", np.shape(pixels))


            default_color_palette = self.current_color_palette
            #mayavi_color_palette = self.current_mayavi_palette


            if self.ids.midiart_Choice.text == "Edges":
                print("Transforming Edges!")
                #IMAGE
                self.edges = cv2.Canny(pixels, 100, 200)

                #self.edges2 = cv2.Canny(pixels2, 100, 200)
                #CONCATENATE with PIANO
                self.preview = midiart.cv2_tuple_reconversion(pixels2,
                                                              inPlace=False,
                                                              conversion ='Edges')[1]
                self.img_with_piano = self.parent.ids.imagedraw_Area.join_with_piano(self.preview)


                #NAME
                self.name = "Edges" + "_" + img_name

                #STREAM
                self.stream = midiart.make_midi_from_grayscale_pixels(self.edges,
                                                                      gran,
                                                                      connect=MIDAS_Settings.connectNotes,
                                                                      note_pxl_value=255)
                                                                      ##dialog.inputKey.GetValue(), , colors=False
                print("EdgeStream:", self.stream)
                self.stream.show('txt')

                #name = str(len(m_v.actors)) + "_" + "Edges" + "_" + dialog.img_name
                print("Edges load completed.")

            if self.ids.midiart_Choice.text == "Color":
                print("Transforming Color!")
                print("PREPixels2:", pixels2)
                print("Gran", gran)
                print("Here.")
                print("DEFAULT_COLOR_PALETTE_2, import.", default_color_palette)
                #The default_color_palette is the dictionary of colors by which our coords must be sorted.

                #IMAGE
                self.colors = pixels2
                self.nn_colors = midiart.set_to_nn_colors(pixels2, MIDAS_Settings.current_color_palette)
                #CONCATENATE with PIANO
                self.img_with_piano = self.parent.ids.imagedraw_Area.join_with_piano(self.nn_colors)

                #NAME
                self.name = "Colors" +  "_" + MIDAS_Settings.color + "_" + img_name

                #STREAM
                #swaprnb = midiart.convert_dict_colors(MIDAS_Settings.current_color_palette, invert=True)
                swaprnb = MIDAS_Settings.current_color_palette
                self.stream = midiart.transcribe_colored_image_to_midiart(self.colors,
                                                                     granularity=gran,
                                                                     connect=MIDAS_Settings.connectNotes,
                                                                     keychoice=MIDAS_Settings.key,
                                                                     colors=swaprnb,
                                                                     output_path=None)
                print("ColorsStream:", self.stream)
                self.stream.show('txt')
                print("Colors load completed.")

            if self.ids.midiart_Choice.text == "Monochrome":
                print("Transforming Monochrome!")
                #IMAGE
                self.monochrome = pixels
                #CONCATENATE with PIANO
                conversion = midiart.cv2_tuple_reconversion(pixels2,
                                                            inPlace=False,
                                                            conversion='Monochrome')
                self.preview = conversion[1]
                self.preview2 = conversion[0]
                # list_1 = [tuple(i) for i in self.preview2]
                # list_2 = [tuple(i) for i in self.monochrome]
                # assert list_1 == list_2, print("These are not the same.") assert failed
                self.img_with_piano = self.parent.ids.imagedraw_Area.join_with_piano(self.preview)

                #NAME
                self.name = "Monochrome" + "_" + img_name  # "QR-BW"

                #STREAM
                self.stream = midiart.make_midi_from_grayscale_pixels(self.preview2,
                                                                      gran,
                                                                      MIDAS_Settings.connectNotes,
                                                                      note_pxl_value=0)
                print("MonochromeStream:", self.stream)
                self.stream.show('txt')
                print("Monochrome load completed.")

            # Strings
            file_path_img = MIDAS_Settings.filepath + os.sep + self.name + ".png"  # str
            file_path_img_with_piano = MIDAS_Settings.filepath + os.sep + self.name + "_with_piano.png"
            # musicode_default_img = MIDAS_Settings.musicode_default

            # Remove existing, if true
            if os.path.exists(file_path_img) is True:
                shutil.rmtree(file_path_img, ignore_errors=True)
            if os.path.exists(file_path_img_with_piano) is True:
                shutil.rmtree(file_path_img_with_piano, ignore_errors=True)


            # Midi to file strings
            filepath_midi = MIDAS_Settings.filepath + os.sep + "midiart_%s.mid" % self.ids.midiart_Choice.text \
                if self.ids.midiart_Choice.text != "Color" else \
                MIDAS_Settings.filepath + os.sep + "midiart_%s" % self.ids.midiart_Choice.text + "_%s.mid" \
                % MIDAS_Settings.color


            if os.path.exists(filepath_midi) is True:
                shutil.rmtree(filepath_midi, ignore_errors=True)

            # Key filtering
            midiart.filter_notes_by_key(self.stream, key=MIDAS_Settings.key, in_place=True)

            #Midi written to file.
            print("CHOICE", self.ids.midiart_Choice.text)
            if self.ids.midiart_Choice.text != "Midiart":
                midiart.set_parts_to_midi_channels(self.stream, filepath_midi) \
                    if self.ids.midiart_Choice.text == "Color" else self.stream.write("mid", filepath_midi)
            else:
                pass

            # Image with midi to file
            cv2.imwrite(file_path_img_with_piano, self.img_with_piano)

            #Update Gui View
            self.parent.ids.imagedraw_Area.ids.image_View.source = file_path_img_with_piano
            #self.parent.ids.imagedraw_Area.ids.image_View.reload()

        else:
            pass

        #KIVY BUG - this clears out an event in my workflow be forcing a change to a str while keeping it the same str.
        #This also forced having to put this entire function in a bool code block so that it doesn't execute multiple
        #times. This entire function will be called when self.ids.midiart_Choice.text is changed. Changing it to itself
        #doesn't actually change it, so I used upper. In code block, if str.isupper(), don't execute. ***Here.
        self.ids.midiart_Choice.text = self.ids.midiart_Choice.text.upper()

        #self.ids.midiart_Choice.text = self.ids.midiart_Choice.text.lower().capitalize()


class MusicodeDrawArea(BoxLayout):
    splash = MIDAS_Settings.welcome
    default_splash = MIDAS_Settings.welcome_default
    musicode_source = ObjectProperty(splash)

        #musicodedraw_Area
    def __init__(self,**kwargs):
        super(MusicodeDrawArea, self).__init__(**kwargs)
        print("self.ids", self.ids)
        print("ids_Type", type(self.ids))
        #print("parent.Ids", self.pareids) #.box_Split.ids.drawarea_Splitter

    def change_image(self, image=MIDAS_Settings.welcome_default):
        print("Changing image.")
        print("self.ids.musicode_View", self.ids.musicode_View)
        print("self.ids.musicode_View.image_source", self.ids.musicode_View.source)
        self.ids.musicode_View.source = image
        self.ids.musicode_View.reload()
        print("image", image)
        print("self.ids.musicode_View.source2", self.ids.musicode_View.source)
        print("Rock On!")
        self.parent.refresh_counter = 0


    def join_with_piano(self, image, piano=MIDAS_Settings.phatpiano2):
        image = image
        piano = cv2.imread(piano) #Remember, cv2.imread swaps rgb to bgr.

        print("IMAGE_ndim", image.ndim)
        print("IMAGE_shape", image.shape)
        musicode_image = np.hstack([piano, image])
        return musicode_image



class ImageDrawArea(BoxLayout):
    splash = MIDAS_Settings.image
    default_splash = MIDAS_Settings.default_image
    #musicode_source = ObjectProperty()
    image_source = ObjectProperty(splash)  #StringProperty?
    #print("self.ids", ids)
    def __init__(self,**kwargs):
        super(ImageDrawArea, self).__init__(**kwargs)
        print("self.ids", self.ids)
        print("ids_Type", type(self.ids))

    def change_image(self, image=MIDAS_Settings.default_image):
        print("Changing image.")
        print("self.ids.image_View", self.ids.image_View)
        print("self.ids.image_View.image_source", self.ids.image_View.source)
        #self.ids.image_View.remove_from_cache()
        #self.ids.image_View = AsyncImage(source = image)
        #self.ids.image_View.reload()
        self.ids.image_View.source = image
        #self.ids.image_View.reload()
        #self.root.ids.mainpage.ids.btn.ids.image_View.source = image
        #self.get_root_window().MidiDrawArea.image_View.source = image
        #reload = self.ids.image_View.reload
        #print("reload", reload)
        print("image", image)
        print("self.ids.image_View.source2", self.ids.image_View.source)
        print("Rock On!")
        self.parent.refresh_counter = 0



    def join_with_piano(self, image, piano=MIDAS_Settings.phatpiano):
        image = image
        piano = cv2.imread(piano)  # Remember, cv2.imread swaps rgb to bgr.

        height = MIDAS_Settings.noteHeight
        width = int(height / len(piano) * len(piano[0]))

        piano = cv2.resize(piano, (width, height), cv2.INTER_AREA)

        print("IMAGE_ndim", image.ndim)
        print("IMAGE_shape", image.shape)
        # piano = cv2.cvtColor(piano, cv2.COLOR_BGR2RGB)   #Keep an EYE on this thang.
        # if len(image) > 127:
        # print("The .png file size is too large. Scaling to height of 127.")
        # height = 127
        # width = int(127 / len(image) * len(image[0]))
        # resizedImg = cv2.resize(image, (width, height), cv2.INTER_AREA)
        musicode_image = np.hstack([piano, image])
        return musicode_image

        # splash = os.getcwd() + os.sep + "MIDAS_Mobile_splash.png"
        # source = StringProperty(splash)


class MainUI(GridLayout):
    def __init__(self,**kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.images_list = list()
        self.refresh_counter = 0


    def refresh(self):
        if self.refresh_counter == 0:
            self.welcome_screen()
            #self.ids.imagedraw_Area.ids.image_View.keep_ratio = True
            self.refresh_counter += 1
        elif self.refresh_counter == 1:
            self.musicode_help_screen()
            self.refresh_counter += 1
        elif self.refresh_counter == 2:
            self.midiart_help_screen()
            self.refresh_counter += 1
        else:
            self.credits_screen()
            #self.refresh_counter += 1


    def reset_inputs(self):
        self.ids.midiart_Buttons.ids.colors_Choice.text = "Select Color"
        self.ids.midiart_Buttons.ids.midiart_Choice.text = "Midiart"
        self.ids.midiart_Buttons.ids.tb_N.state = "normal"
        self.ids.midiart_Buttons.ids.tb_Y.state = "down"
        self.ids.midiart_Buttons.ids.txt_Key.text = "Key"
        self.ids.midiart_Buttons.ids.granularity_Choice.text = "Note Durations"
        self.ids.midiart_Buttons.ids.note_Height.text = str(127)

        self.ids.musicode_Area.ids.musicode_Choice.text = '  Select \n\nA Musicode'
        self.ids.musicode_Area.ids.txt_Input.text = ""

        reload(MIDAS_Settings)


    def assert_for_inputs(self):
        assertion_list = [self.ids.midiart_Buttons.ids.colors_Choice.text == 'Select Color',
        self.ids.midiart_Buttons.ids.midiart_Choice.text is "Midiart",
        self.ids.midiart_Buttons.ids.tb_N.state is "normal",
        self.ids.midiart_Buttons.ids.tb_Y.state is "down",
        self.ids.midiart_Buttons.ids.txt_Key.text is "Key",
        self.ids.midiart_Buttons.ids.granularity_Choice.text == "Note Durations",
        self.ids.midiart_Buttons.ids.note_Height.text is '127',
        self.ids.musicode_Area.ids.musicode_Choice.text == '  Select \n\nA Musicode',
        self.ids.musicode_Area.ids.txt_Input.text is ""]

        assertion_list2 = [self.ids.midiart_Buttons.ids.colors_Choice.text,
        self.ids.midiart_Buttons.ids.midiart_Choice.text,
        self.ids.midiart_Buttons.ids.tb_N.state,
        self.ids.midiart_Buttons.ids.tb_Y.state,
        self.ids.midiart_Buttons.ids.txt_Key.text,
        self.ids.midiart_Buttons.ids.granularity_Choice.text,
        self.ids.midiart_Buttons.ids.note_Height.text,
        self.ids.musicode_Area.ids.musicode_Choice.text,
        self.ids.musicode_Area.ids.txt_Input.text]

        print("Assertion_List: -->", assertion_list)
        print("Assertion_List2: -->", assertion_list2)
        for i in assertion_list:
            if i is False:
                return i


    def welcome_screen(self):
        print("Welcome Screen")
        if self.assert_for_inputs() is False:
            self.reset_inputs()
            print("Inputs Reset")


        self.ids.musicodedraw_Area.change_image()
        self.ids.musicodedraw_Area.ids.musicode_View.reload()

        self.ids.imagedraw_Area.change_image()
        self.ids.imagedraw_Area.ids.image_View.reload()

        #self.ids.imagedraw_Area.ids.image_View.keep_ratio = False

        #self.musicode_area = MusicodeArea()
        #self.midiart_buttons = MidiArtButtons()
        #self.midi_draw_area = MidiDrawArea()


    def musicode_help_screen(self):
        print("Musicode Help Screen")
        if self.assert_for_inputs() is False:
            self.reset_inputs()
            print("Inputs Reset")

        self.ids.musicodedraw_Area.change_image(MIDAS_Settings.musicode_banner)
        self.ids.musicodedraw_Area.ids.musicode_View.reload()


        self.ids.imagedraw_Area.ids.image_View.keep_ratio = False
        self.ids.imagedraw_Area.change_image(MIDAS_Settings.musicodes_visual)
        self.ids.imagedraw_Area.ids.image_View.reload()


    def midiart_help_screen(self):
        print("Midiart Help Screen")
        if self.assert_for_inputs() is False:
            self.reset_inputs()
            print("Inputs Reset")

        self.ids.musicodedraw_Area.change_image(MIDAS_Settings.midiart_banner)
        self.ids.musicodedraw_Area.ids.musicode_View.reload()

        self.ids.imagedraw_Area.change_image(MIDAS_Settings.midiart_visual)
        self.ids.imagedraw_Area.ids.image_View.reload()


    def credits_screen(self):
        print("Credits Screen")
        if self.assert_for_inputs() is False:
            self.reset_inputs()
            print("Inputs Reset")

        self.ids.musicodedraw_Area.change_image(MIDAS_Settings.credits_banner)
        self.ids.musicodedraw_Area.ids.musicode_View.reload()

        self.ids.imagedraw_Area.change_image(MIDAS_Settings.credits_visual)
        self.ids.imagedraw_Area.ids.image_View.reload()
        self.refresh_counter = 0
        #self.ids.imagedraw_Area.ids.image_View.keep_ratio = True


class MIDASApp(App):
    def __init__(self,**kwargs):
        super(MIDASApp, self).__init__(**kwargs)
        self.title = "MIDAS Mobile"


    def build(self):
        return MainUI()



Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    MIDASApp().run()
