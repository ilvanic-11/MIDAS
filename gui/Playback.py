##A module with methods for playing back midifiles outed to device on the soundcard.

###NOTE: IMPORTANT STUFF
#quarterLengthDivisor---DETERMINES QUANTIZATION and THUS the PRESERVATION OF NOTES THAT ARE PARSED FROM A MIDI FILE.
# import threading
# import asyncio
# import itertools
#
# import music21

# sparklead1 = r"resources\OneSpark.mid"
# spark21 = music21.converter.parse(sparklead1, quantizePost=True, quarterLengthDivisors=(8,6), makeNotation=True)

#import pygame
#import mido
#import pyo
#import gui.Preferences

#from midas_scripts import midiart
import pyo
import pyo.lib.server
from pyo.lib import _wxwidgets
#pyo.PYO_USE_WX = False

import mido
from wx import Timer as wxTimer
import os
import time
import sys
#from pyo.lib.server import Server
from traits.api import Any, HasTraits, Button, Range  ##Instance,
from traitsui.api import View, Group, Item

#from gui import Patch
from gui.Patch import InfiniteTimer  #uses threading.Timer
from gui.Patch import mpInfiniteTimer   #uses a multiprocessing-derived Timer
from gui.Patch import wxInfiniteTimer   #uses a wx.Timer()
from gui.Patch import on_quit, on_quit1

#####################################################
####METHOD 1----Complete Working Method.
######################################################
#sparklead3 = r"resources\Spark6Lead.mid"
#wishyouwerehere = r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\Game Midi Downloads\Pink_Floyd_-_Wish_You_Were_Here.mid"
#pyo.pa_list_devices()



class Player():
    """A class object for midi playback via a python generator and a simple pyo synthesizer. Class must be instantiated
    with a midifile input."""
    def __init__(self, midifilepath=None, parent=None, bpm=None, waveform='Sine', play_now=True, from_gui=False, multi_server=False, player=True):   #TODO Multi-server stuff.
        self.midifilepath = midifilepath
        self.mid = None
        try:
            if midifilepath is not None:
                self.mid = mido.MidiFile(midifilepath)
        except:
            self.mid = None
        if parent is None:
            self.server = pyo.Server()
        else:
            self.parent = parent
            self.server = parent.server
        #self.server.setOutputDevice(pyo.pa_get_default_output())  #Set audio output device. This can be configured manually by the user.
                                         #Use self.server.pa_list_devices() to see the outs available to you.
        self.server.boot()    ###.start()

        self.establish_synthesizer(waveform=waveform)

        #Bool determining what version of InfiniteTimer methodology to use.
        self.player = player

        #All attributes must be established before self.open_gui() is called.
        if play_now:
            #self.load_midifile(midifile=midifile, bpm=bpm, from_gui=from_gui)
            self.create_generator()
            self.open_gui()
        else:
            pass


        #self.mainThread = threading.currentThread()
        #self.timerThread =

    #TODO Redundant? Currently implementing method to have timesignature objects and metronomeMark objects in the streams
    # that write to ('mid') file.
    def reset_midi_header(self, midifile, from_gui=False):
        """This function requires a source midifile called 'Default_Midi_Header.mid'. It gives the midi file necessary
        midi musical information.

        :param midifile:
        :return: 
        """
        if self.mid is None:
            self.mid = mido.MidiFile(midifile)
        else:
            pass
        intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
        midi_header = mido.MidiFile(intermediary_path + "Default_Midi_Header.mid")
        if from_gui:
            midi_header.tracks.append(self.mid.tracks[0])
            self.mid = midi_header
        else:
            if len(self.mid.tracks) > 1:
                track_1 = self.mid.tracks[1]
                self.mid.tracks[0] = midi_header.tracks[0]
                self.mid.tracks.append(track_1)
                #self.mid.tracks.append(midi_header.tracks[0])
            elif len(self.mid.tracks) == 0:
                track = self.mid.tracks[0]
                self.mid.tracks[0] = midi_header.tracks[0]
                self.mid.tracks.append(track)
        return self.mid


    def load_midifile(self, midifile, bpm, from_gui=False):
        self.mid = self.reset_midi_header(midifile, from_gui=from_gui)
        self.change_tempo(bpm)


    def create_generator(self):
        m_v = self.parent.mayavi_view
        assert self.parent is not None, print("You must supply a wx window or frame as self.parent.")
        self.timer = InfiniteTimer(seconds=0, target=self.yield_midi().__next__, window=self.parent, player=self.player) #.__next__  Infinite  wx   seconds=0, target=   itertools.tee(   , 1)[0]
        self.timer.start()
        self.timer.stop()
        ### Overloads (using redefined methods ^)
        #self.timer2 = InfiniteTimer(seconds=0, target=m_v.generate_plane_scroll(m_v.grid3d_span, m_v.bpm, m_v.frames_per_beat).__next__)


    def open_gui(self):
        self.server.start = self.start
        self.server.stop = self.stop

        print("Here5")
        print("shutdown method", self.server.shutdown)

        self.server.shutdown = self.shutdown

        print("shutdown method", self.server._server.shutdown)
        print("Here6")

        #FORCED WORKAROUND -- original code restored at end of use.
        _wxwidgets.ServerGUI.on_quit = on_quit1
        print("Here7")

        self.server.gui(locals(), exit=False)  #If exit=True, the entire Midas app will shutdown.
        print("Here8")

        #self.server.shutdown = self.quit
        #self.server.closeGui = self.quit
        #self.server.stop()
        #self.server._server.on_quit = self.quit
        #self.server._server.shutdown()


    #Initiate pyo server for hosting\processing real-time audio\midi.


    #Establish new start and stop methods.
    def start(self):
        """
        Start the audio callback loop and begin processing.
        Start the midi generator function.
        """
        #self.parent.mayavi_view.scene3d.disable_render = True
        print("Here 2")

        self.server._server.start()

       #self.timer.thread.
        print("Here 3")

        self.timer.start()   #start()
        #self.timer2.start()
        print("Here 4")

        self.parent.planescroll_animator._start_fired()

        # c_timer.start()
        # anim._start_fired()
        return self.server._server



    def stop(self):
        """
        Stop the audio callback loop.
        Stop the midi generator function.
        """
        #self.parent.mayavi_view.scene3d.disable_render = False

        self.parent.planescroll_animator._stop_fired()
        self.server._server.stop()
        self.timer.stop()  #stop()

        #self.timer.thread.finished.set()
        #self.timer2.cancel()

        # c_timer.stop()
        # anim._start_fired()

    #Overwriter
    def shutdown(self):  # The server's method is called shutdown. We will rebind that.

        self.parent.mayavi_view.reset_volume_slice(self.parent.mayavi_view.grid3d_span, volume_slice=True)
        print("Volume slice reset.")


        #We make the shutdown happen anyway.
        self.server._server.shutdown()
        print("Server shutdown.")

        self.server = None  # self.server._server
        if os.path.isfile(self.midifilepath):
            os.remove(self.midifilepath)
        print("Playback ended, gui closed, temp_file deleted.")
                                                    # TODO Figure out why I can never get here......CHECK
                                                    #  parameter 'self.exit' was false in _wxwidgets.ServerGUI.on_quit
                                                    #  when it should have been True.

        #Restore original code here, so if the _wxwidgets gui is used again else where in the program,
        #it won't run into problems from this workaround.
        #Written this way to preserve code as it was pipinstalled.
        _wxwidgets.ServerGUI.on_quit = on_quit
        print("Overwrite of 'on_quit' function restored to original.")


    def change_tempo(self, bpm):
        if bpm is None:
            pass
        elif self.mid is None:
            print("Midifile not yet loaded.")
        else:
            self.mid.tracks[0][0].tempo = mido.bpm2tempo(bpm)


    #### Opening the MIDI file. Here we use a generator function that fires our midi messages with the assistance
    #    of InfiniteTimer.

    #### ... and reading its content.
    #@mlab.animate(delay=0, ui=True, support_movie=False)    ##Because f*(*&k movies in this context....
    def yield_midi(self):  ##, ipw_position):
        #m_v = self.parent.mayavi_view

        #yield from  self.parent.mayavi_view.generate_plane_scroll(m_v.grid3d_span, m_v.bpm, m_v.frames_per_beat)
        for message in self.mid.play():
            #Todo Put generate_plane_scroll generator here? With sleep value set to message.sleep?
            # print("Midi_Gen_Thread", threading.currentThread())
            # print("Midi_Gen_Thread_Name", threading.currentThread().getName())
            # print("Midi_Gen_allThreads", threading.enumerate())
            # print("Midi_Gen_allThreads", threading.active_count())
            print("MIDI_GEN")
            yield self.server.addMidiEvent(*message.bytes())
            #yield # from #ipw_position

    #Generator\server is stopped immediately, allowing user to control it at their leisure.

    def establish_synthesizer(self, waveform):
        # A little audio synth to play the MIDI events.
        # This pyo synth stuff has ENORMOUS potential to be highly modable.
        self.midz = pyo.Notein(poly=127)  #Set poly to 127 to handle polyphonies of up to 127 simultaneous notes, exactly what we want.
        self.amp = pyo.MidiAdsr(self.midz["velocity"])
        self.pit = pyo.MToF(self.midz["pitch"])
        print("Waveform", waveform)
        if waveform != "Saw" or waveform != "Square" or waveform != "Triangle":
            self.osc = pyo.Sine(freq=self.pit, mul=self.amp).mix(1)
        else:
            waveform = eval("pyo.%sTable()" % waveform)
            self.osc = pyo.Osc(waveform, freq=self.pit, mul=self.amp).mix(1)
        self.rev = pyo.STRev(self.osc, revtime=1, cutoff=4000, bal=0.2).out()
        return self.osc


###################
# Animator Re-write
###################
#TODO Sync with preferences Animator patch.
class Animator(HasTraits):
    """ Convenience class to manage a timer and present a convenient
        UI.  This is based on the code in `tvtk.tools.visual`.
        Here is a simple example of using this class::

            >>> from mayavi import mlab
            >>> def anim():
            ...     f = mlab.gcf()
            ...     while 1:
            ...         f.scene.camera.azimuth(10)
            ...         f.scene.render()
            ...         yield
            ...
            >>> anim = anim()
            >>> t = Animator(500, anim.__next__)
            >>> t.edit_traits()

        This makes it very easy to animate your visualizations and control
        it from a simple UI.

        **Notes**

        If you want to modify the data plotted by an `mlab` function call,
        please refer to the section on: :ref:`mlab-animating-data`
    """

    ########################################
    # Traits.

    start = Button('Start Animation')
    stop = Button('Stop Animation')
    delay = Range(0, 100000, 500,  # Isaac edit
                  desc='frequency with which timer is called')

    # The internal timer we manage.
    timer = Any

    ######################################################################
    # User interface view

    traits_view = View(Group(Item('start'),
                             Item('stop'),
                             show_labels=False),
                       Item('_'),
                       Item(name='delay'),
                       title='Animation Controller',
                       buttons=['OK'])

    ######################################################################
    # Initialize object
    def __init__(self, millisec, callable, window,  *args, **kwargs):  # timer_delay,   player,
        r"""Constructor.

        **Parameters**

          :millisec: int specifying the delay in milliseconds
                     between calls to the callable.

          :callable: callable function to call after the specified
                     delay.

          :\*args: optional arguments to be passed to the callable.

          :\*\*kwargs: optional keyword arguments to be passed to the callable.

        """
        HasTraits.__init__(self)
        self.delay = millisec
        self.ui = None
        self.timer = InfiniteTimer(millisec, callable, window)  ##, #player)  #wx mp timer_delay

    ######################################################################
    # `Animator` protocol.
    ######################################################################
    def show(self):
        """Show the animator UI.
        """
        self.ui = self.edit_traits()

    def close(self):
        """Close the animator UI.
        """
        if self.ui is not None:
            self.ui.dispose()

    ######################################################################
    # Non-public methods, Event handlers
    def _start_fired(self):
        self.timer.start()  ###self.delay

    def _stop_fired(self):
        self.timer.stop()

    # def _delay_changed(self, value):
    #     t = self.timer
    #     if t is None:
    #         return
    #     if t.IsRunning():
    #         t.stop()
    #         t.start(value)





    #### Display server gui.  (NOTE: I had to modify their source code to get this to work)

#Playback(sparklead3, bpm=None)


    # delay = Range(10, 100000, 500,
    #               desc='frequency with which timer is called')

        # for message in mid.play():
        # For each message, we convert it to integer data with the bytes()
        # method and send the values to pyo's Server with the addMidiEvent()
        # method. This method programmatically adds a MIDI message to the
        # server's internal MIDI event buffer.

    #s.setCallback(execute_play)

#############
#Generate Single-Instance Midi Data function
#############

# def generate_midi_data(midifile, bpm=120, data=1, iter=False, filterOFFevents=True):
#         """
#             This is a special function. It's my favorite.
#             Generator\ object to generate the specific individual elements of a midifile, message by message.
#         (0--DeltaTimeON\OFF, 1--PITCH, 2--VELOCITY, 3--DELAY(TIME--in microseconds? from the last NOTEOFF event)
#         This generator object is intelligent. It uses mido.Midifile().play() to generate the midievents
#         programmatically. Thus if iter is false, the generated data will be generated in tempo with the correct delays
#         between ON\\OFF events.-
#         :param midifile:            Midifile from which to create generator.
#         :param bpm:                 The tempo in beats per minute at which to generate the midi messages. If iter is
#                                     True, this is irrelevant. (Still useful to manually set the midifile's tempo.)
#         :param data:                The type of data to be generated\extracted.
#         :param iter:                Determines whether internal call to 'mid' variable is an iterator or a generator.
#                                     This therefore determines speed of acquiring the generated data.
#         :param filterOFFevents:     For the output, this takes out the values that would have been acquired from note
#                                     OFF events
#         :return:                    Generator object.
#         """
#
#         import mido
#
#         # Opening the MIDI file...
#         mid = mido.MidiFile(midifile)
#
#         # Handle tempo manually, if desired.
#
#         mid.tracks[0][0].tempo = mido.bpm2tempo(bpm)
#
#         # Delay thing for synths
#
#         # Data check, cannot be outside range of 0,1,2, or 3
#         assert 0 <= data < 4, "Data type must be within specified range of the following ints:  0(Note On\Off), 1(Pitch), 2(Velocity), or 3(Time\Delay)"
#
#         if iter:
#             # Change this to just mid: instead mid.play(): for iteration instead of generation.
#             for message in mid:
#                 if filterOFFevents is True:
#                     if not message.is_meta:
#
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.time
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#                 else:
#                     if not message.is_meta:
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.time
#                     # yield print(message)
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#         else:
#             for message in mid.play(
#                     meta_messages=True):  # .play() yields this values according to the message.time value, ergo programmatically.
#                 if filterOFFevents is True:
#                     if not message.is_meta:
#
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.time
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#                 else:
#                     if not message.is_meta:
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.time
#                     # yield print(message)
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break

    #ON\OFF

    # s.addMidiEvent([i for i in generate_midi(midifile, bpm=160, data=0, iter=True)], [i for i in generate_midi(midifile, bpm=160, data=1, iter=True)], [i for i in generate_midi(midifile, bpm=160, data=2, iter=True)])
    #lead_status = [i for i in generate_midi_data(midifile, bpm=160, data=0, iter=True, filterOFFevents=False)]
    #Time
    #lead_dur = [j for j in generate_midi_data(midifile, bpm=160, data=3, iter=True, filterOFFevents=False)]
    #Pitch
    #lead_midi = [i for i in generate_midi_data(midifile, bpm=160, data=1, iter=True, filterOFFevents=False)]
    #Velocity
    #lead_vel = [k for k in generate_midi_data(midifile, bpm=160, data=2, iter=True, filterOFFevents=False)]




# ########################################################
# ####METHOD 2 -- Pygame method.
# ########################################################
# freq = 44100  # audio CD quality
# bitsize = -16   # unsigned 16 bit
# channels = 2  # 1 is mono, 2 is stereo
# buffer = 1024   # number of samples
# pygame.mixer.init(freq, bitsize, channels, buffer)
# sparklead = r"resources\Spark4Lead.mid"
#
# def play_music(midi_filename):
#     '''Stream music_file in a blocking manner'''
#     clock = pygame.time.Clock()
#     pygame.mixer.music.load(midi_filename)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         clock.tick(30)  # check if playback has finished
#
# ##Execute
# try:
#   # use the midi file you just saved
#   play_music(sparklead)
# except KeyboardInterrupt:
#   # if user hits Ctrl/C then exit
#   # (works only in console mode)
#   pygame.mixer.music.fadeout(1000)
#   pygame.mixer.music.stop()
#   raise SystemExit
#
# #####################################################
# ####METHOD 2----Original Method, doesn't have gui buttons for start and stop.
# ######################################################
# sparklead3 = r"resources\Spark6Lead.mid"
# def setup_server_and_play_oscillator(midifile):
#     import pyo
#     import mido
#     from midas_scripts import music21funcs
#     # Try to import MidiFile from the mido module. You can install mido with pip:
#     #   pip install mido
#     try:
#         from mido import MidiFile
#     except:
#         print("The `mido` module must be installed to run this example!")
#         exit()
#     s = pyo.Server().boot().start()
#
#     def generate_midi_data(midifile, bpm=120, data=1, iter=False):
#         """
#             Generator\iterator object to generate the specific individual elements of a midifile, message by message.
#         (0--DeltaTimeON\OFF, 1--PITCH, 2--VELOCITY, 3--DELAY(TIME--in microseconds from the last NOTEOFF event)
#         This generator object is intelligent. It uses mido.Midifile().play() to generate the midievents programmatically.
#         Thus, if iter is false, the generated data will be generated in tempo with the correct delays between ON\OFF events.
#         :param midifile:    Midifile from which to create generator.
#         :param bpm:         The tempo in beats per minute at which to generate the midi messages. If iter is True,
#                             this is irrelevant. (Still useful to manually set the midifile's tempo.)
#         :param data:        The type of data to be generated\extracted.
#         :return: Generator\iterable object.
#         """
#
#         import mido
#         mid = mido.MidiFile(midifile)
#
#         #Handle tempo manually, if desired.
#         mid.tracks[0][0].time = mido.bpm2tempo(bpm)
#
#         #Data check, cannot be outside range of 0,1,2, or 3
#         assert 0 <= data < 4, "Data type must be within specified range of the following ints:  0(Note On\Off), 1(Pitch), 2(Velocity), or 3(Time\Delay)"
#
#         if iter:
#         #Change this to just mid: instead mid.play(): for iteration instead of generation.
#             for message in mid:
#                 if data != 3:
#                     if not message.is_meta:
#                             #isinstance(message, mido.midifiles.meta.MetaMessage):
#                         yield message.bytes()[data]
#                 else:
#                     if not message.is_meta:
#                             #isinstance(message, mido.midifiles.meta.MetaMessage):
#                         yield message.time
#         else:
#             for message in mid.play():  # .play() yields this values according to the message.time value, ergo programmatically.
#                 if data != 3:
#                     if not message.is_meta:
#                             #isinstance(message, mido.midifiles.meta.MetaMessage):
#                         yield message.bytes()[data]
#                 else:
#                     if not message.is_meta:
#                             #isinstance(message, mido.midifiles.meta.MetaMessage):
#                         yield message.time
#
# # A little audio synth to play the MIDI events.
#     mid = pyo.Notein()
#     amp = pyo.MidiAdsr(mid["velocity"])
#     pit = pyo.MToF(mid["pitch"])
#     print("PIT", pit)
#     osc = pyo.Osc(pyo.SawTable(), freq=pit, mul=amp).mix(1)
#     rev = pyo.STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()
#
#     # Opening the MIDI file...
#     mid = mido.MidiFile(midifile)
#
#     # ... and reading its content.
#     ## def execute_play():
#     ##     for message in mid.play():
#     ##         s.addMidiEvent(*message.bytes())
#
#     #Display server gui.  (NOTE: I had to modify their source code to get this to work)
#
#     #s.addMidiEvent([i for i in generate_midi(midifile, bpm=160, data=0, iter=True)], [i for i in generate_midi(midifile, bpm=160, data=1, iter=True)], [i for i in generate_midi(midifile, bpm=160, data=2, iter=True)])
#     #s.gui(locals(), exit=False)
#
#     for message in mid.play():
#         s.addMidiEvent(*message.bytes())
#         # for message in mid.play():
#         # For each message, we convert it to integer data with the bytes()
#         # method and send the values to pyo's Server with the addMidiEvent()
#         # method. This method programmatically adds a MIDI message to the
#         # server's internal MIDI event buffer.
#
#     #s.setCallback(execute_play)
#
#
# setup_server_and_play_oscillator(sparklead3)
#
#
# #####################################################
# ####METHOD 4----Attempt at DYNAMIC Method! (Doesn't do polyphony yet) TODO Make polyphony work.
# ######################################################
#
# sparklead3 = r"resources\Spark6Lead.mid"
# onespark = r"resources\OneSpark.mid"
# def setup_server_and_play_oscillator2(midifile, bpm):
#     import pyo
#     import mido
#     from midas_scripts import music21funcs
#     # Try to import MidiFile from the mido module. You can install mido with pip:
#     #   pip install mido
#     try:
#         from mido import MidiFile
#     except:
#         print("The `mido` module must be installed to run this example!")
#         exit()
#
#     one_quarter_delay = 60 / bpm  # time per beat in seconds
#
#     def generate_midi_data(midifile, bpm=120, data=1, iter=False, filterOFFevents=True):
#         """
#             This is a special function. It's my favorite.
#             Generator\ object to generate the specific individual elements of a midifile, message by message.
#         (0--DeltaTimeON\OFF, 1--PITCH, 2--VELOCITY, 3--DELAY(TIME--in microseconds? from the last NOTEOFF event)
#         This generator object is intelligent. It uses mido.Midifile().play() to generate the midievents
#         programmatically. Thus if iter is false, the generated data will be generated in tempo with the correct delays
#         between ON\\OFF events.-
#         :param midifile:            Midifile from which to create generator.
#         :param bpm:                 The tempo in beats per minute at which to generate the midi messages. If iter is
#                                     True, this is irrelevant. (Still useful to manually set the midifile's tempo.)
#         :param data:                The type of data to be generated\extracted.
#         :param iter:                Determines whether internal call to 'mid' variable is an iterator or a generator.
#                                     This therefore determines speed of acquiring the generated data.
#         :param filterOFFevents:     For the output, this takes out the values that would have been acquired from note
#                                     OFF events
#         :return:                    Generator object.
#         """
#
#         import mido
#
#         # Opening the MIDI file...
#         mid = mido.MidiFile(midifile)
#
#         #Handle tempo manually, if desired.
#
#         mid.tracks[0][0].tempo = mido.bpm2tempo(bpm)
#
#         #Delay thing for synths
#
#
#         #Data check, cannot be outside range of 0,1,2, or 3
#         assert 0 <= data < 4, "Data type must be within specified range of the following ints:  0(Note On\Off), 1(Pitch), 2(Velocity), or 3(Time\Delay)"
#
#         if iter:
#         #Change this to just mid: instead mid.play(): for iteration instead of generation.
#             for message in mid:
#                 if filterOFFevents is True:
#                     if not message.is_meta:
#
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.time
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#                 else:
#                     if not message.is_meta:
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.time
#                     # yield print(message)
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#         else:
#             for message in mid.play(meta_messages=True):  # .play() yields this values according to the message.time value, ergo programmatically.
#                 if filterOFFevents is True:
#                     if not message.is_meta:
#
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             if 144 <= message.bytes()[0] <= 159:
#                                 yield message.time
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#                 else:
#                     if not message.is_meta:
#                         if data != 3:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.bytes()[data]
#                         else:
#                             # isinstance(message, mido.midifiles.meta.MetaMessage):
#                             yield message.time
#                     #yield print(message)
#                     elif message.is_meta and message is not mid.tracks[0][-1]:
#                         continue
#                     else:
#                         print(message)
#                         break
#
#     s = pyo.Server().boot()
#
#
#     #s.deactivateMidi()
#     #s.start()
#
#     #Manual Methods
#     #lead_midi = [65, 65, 63, 65, 67, 60, 63, 65, 65, 63, 65, 67, 60, 63, 70, 67, 65, 63, 70, 67, 65, 63, 65]
#     # lead_beat = [2, 1.5, 0.5, 0.5, 1, 1, 1.5, 2, 1.5, 0.5, 0.5, 1, 1, 1.5, 0.5, 1, 1, 1.5, 0.5, 1, 1, 1.5, 8]
#     #lead_decay = [0.045, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 1.625]
#
#     #Midi Generation method (in progress)
#     lead_midi2 = [i for i in generate_midi_data(midifile, bpm=bpm, data=1, iter=True, filterOFFevents=True )]
#     lead_dur = [j for j in generate_midi_data(midifile, bpm=bpm, data=3, iter=True, filterOFFevents=True)]
#     lead_vel = [k for k in generate_midi_data(midifile, bpm=bpm, data=2, iter=True, filterOFFevents=True)]
#
#
#     print("Midi2", lead_midi2)
#     print("Length2", len(lead_midi2))
#     print("Dur", lead_dur)
#     print("Length", len(lead_dur))
#     print("Velocity", lead_vel)
#     print("Length", len(lead_vel))
#
#     lead_midi = []
#     lead_beat = []
#     lead_decay = []
#
#     parse1 = music21.converter.parse(midifile, quantizePost=True, quarterLengthDivisors=(8, 6),
#                                      makeNotation=True)
#     parse2 = music21funcs.notafy(parse1)
#     #Done in one loop, so I don't have to call converter.parse twice.
#     for i in parse2.flat.notes:
#         lead_midi.append(i.pitch.ps)
#         lead_beat.append(i.quarterLength)
#         lead_decay.append(i.quarterLength/2.65)
#
#
#     print("Midi", lead_midi)
#     print("Length", len(lead_midi))
#     print("Beat", lead_beat)
#     print("Length", len(lead_beat))
#     print("Decay?", lead_decay)
#     print("Length", len(lead_decay))
#
#
#     ############
#     #SYNTHS
#     ############
#     # A 2nd synth, defined as a class.
#     class LeadSynth(pyo.EventInstrument):
#         def __init__(self, **args):
#             pyo.EventInstrument.__init__(self, **args)
#
#             self.phase = pyo.LFO([self.freq, self.freq * 1.003], type=3)
#
#             self.duty = pyo.Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
#
#             self.osc = pyo.Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)
#
#             self.filt = pyo.Biquad(self.osc, freq=4000, q=1, mul=self.env).out()
#
#     # A simple custom instrument. Note that the out() method is not called!
#     class MyInstrument(pyo.EventInstrument):
#         def __init__(self, **args):
#             pyo.EventInstrument.__init__(self, **args)
#             self.output = pyo.LFO(freq=self.freq, sharp=[0.5, 0.6], type=2, mul=self.env).out()   #WATCH OUT!
#
#     # # A little audio synth to play the MIDI events.
#     # mid = pyo.Notein()
#     # amp = pyo.MidiAdsr(mid["velocity"])
#     # pit = pyo.MToF(mid["pitch"])
#     # #print("PIT", pit)
#     # osc = pyo.Osc(pyo.SawTable(), freq=pit, mul=amp).mix(1)
#     # rev = pyo.STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()
#
#
#     a1 = pyo.Events(instr=MyInstrument,
#                     midinote=pyo.EventSeq(lead_midi2, occurrences=1),
#                     dur=pyo.EventSeq(lead_dur, occurrences=1),
#                     midivel=pyo.EventSeq(lead_vel, occurrences=1),
#                     db=-20.0,  outs=2,   #signal='output', ###beat=pyo.EventSeq(lead_beat, occurrences=1),
#                     attack=0.002, decay=pyo.EventSeq(lead_decay, occurrences=pyo.inf), sustain=0.003, release=0.025, bpm=bpm) \
#         .play(delay=0)
#
#
#
#     # ... and reading its content.
#     ## def execute_play():
#     ##     for message in mid.play():
#     ##         s.addMidiEvent(*message.bytes())
#     #for message in mid.play():
#         #s.addMidiEvent(*message.bytes())
#         # for message in mid.play():
#         # For each message, we convert it to integer data with the bytes()
#         # method and send the values to pyo's Server with the addMidiEvent()
#         # method. This method programmatically adds a MIDI message to the
#         # server's internal MIDI event buffer.
#         #   s.addMidiEvent(*
#
#     #s.setCallback(execute_play)
#
#     #Display server gui.  (NOTE: I had to modify their source code to get this to work)
#     s.gui(locals(), exit=False)
#
#
# ##Execute
# setup_server_and_play_oscillator2(onespark, 160)
#
#
#
#
# #########################################################
# ####BLINDING LIGHTS by The Weeknd EXAMPLE
# #########################################################
# from pyo import *
#
# server = Server().boot()
#
# one_quarter_delay = 60 / 171.0
#
# kick_midi = [10, 10, 10, 10, 10]
# kick_beat = [2, 2, 2, 1 / 2., 3 / 2.]
#
#
# class Kick(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)
#
#         self.phase = Sine([self.freq, self.freq * 1.003])
#
#         self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
#
#         self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-6.0)
#
#         self.filt = Tone(self.osc, freq=100, mul=self.env).out()
#
#
# k = Events(instr=Kick,
#            midinote=EventSeq(kick_midi),
#            beat=EventSeq(kick_beat, occurrences=inf), db=-10.,
#            attack=0.00001, decay=0.005, sustain=0, release=0.005, bpm=171) \
#     .play(delay=32 * one_quarter_delay)
#
# snare_midi = [0, 60, 60, 60, 60]
# snare_beat = [1, 2, 2, 2, 1]
#
#
# class Snare(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)
#
#         self.phase = LFO([self.freq, self.freq * 1.003], type=1)
#
#         self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
#
#         self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-3.)
#
#         st_one = Tone(self.osc, freq=10000, mul=self.env)
#
#         self.filt = Freeverb(st_one, size=0.001, damp=0.9, bal=0.5, mul=1, add=0).out()
#
#
# s = Events(instr=Snare,
#            midinote=EventSeq(snare_midi),
#            beat=EventSeq(snare_beat, occurrences=inf), db=EventSeq([-100.0, -10, -10, -10, -10]),
#            attack=0.002, decay=0.005, sustain=0.003, release=0.001, bpm=171) \
#     .play(delay=32 * one_quarter_delay)
#
# lead_midi = [65, 65, 63, 65, 67, 60, 63, 65, 65, 63, 65, 67, 60, 63, 70, 67, 65, 63, 70, 67, 65, 63, 65]
# lead_beat = [2, 1.5, 0.5, 0.5, 1, 1, 1.5, 2, 1.5, 0.5, 0.5, 1, 1, 1.5, 0.5, 1, 1, 1.5, 0.5, 1, 1, 1.5, 8]
# lead_decay = [0.72, 0.54, 0.18, 0.18, 0.36, 0.36, 0.54, 0.72, 0.54, 0.18, 0.18, 0.36, 0.36, 0.54, 0.18, 0.36, 0.36,
#               0.54, 0.18, 0.36, 0.36, 0.54, 1]
#
#
# class LeadSynth(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)
#
#         self.phase = LFO([self.freq, self.freq * 1.003], type=4)
#
#         self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
#
#         self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)
#
#         self.filt = Biquad(self.osc, freq=4000, q=1, mul=self.env).out()
#
#
# l = Events(instr=LeadSynth,
#            midinote=EventSeq(lead_midi),
#            beat=EventSeq(lead_beat, occurrences=2), db=-20.0,
#            attack=0.003, decay=EventSeq(lead_decay, occurrences=inf), sustain=0.001, release=0.5, bpm=160) \
#     .play(delay=64 * one_quarter_delay)
#
# bass_midi = [34, 32, 31, 29, 27, 29, 24, 27, 27, 29, 22]
# bass_beat = [1.5, 1.5, 1.0, 6.5, 0.5, 0.5, 8.5, 6.5, 0.5, 0.5, 4.5]
#
#
# class BassSynth(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)
#
#         self.phase = LFO([self.freq, self.freq * 1.003], type=1)
#
#         self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=1).play()
#
#         self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)
#
#         self.filt = Tone(self.osc, freq=300, mul=self.env).out()
#
#
# b = Events(instr=BassSynth,
#            midinote=EventSeq(bass_midi),
#            beat=EventSeq(bass_beat, occurrences=inf), db=-12.,
#            attack=0.01, decay=0.001, sustain=0.5, release=0.00001, bpm=171) \
#     .play(delay=28 * one_quarter_delay)
#
#
# class PadSynth(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)
#
#         self.phase = Sine([self.freq, self.freq * 1.003])
#
#         self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
#
#         self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)
#
#         self.filt = Biquad(self.osc, freq=1500, q=1, mul=self.env).out()
#
#
# pad_midi_1 = [56, 48, 46, 46]
# pad_midi_2 = [60, 51, 51, 50]
# pad_midi_3 = [65, 55, 55, 53]
#
# pad_beat = [8, 8, 8, 8]
# pad_db = -32.0
#
# c1 = Events(instr=PadSynth,
#             midinote=EventSeq(pad_midi_1),
#             beat=EventSeq(pad_beat, occurrences=inf), db=pad_db,
#             attack=0.1, decay=0.01, sustain=0.5, release=0.00001, bpm=171) \
#     .play()
#
# c2 = Events(instr=PadSynth,
#             midinote=EventSeq(pad_midi_2),
#             beat=EventSeq(pad_beat, occurrences=inf), db=pad_db,
#             attack=0.1, decay=0.01, sustain=0.5, release=0.00001, bpm=171) \
#     .play()
#
# c3 = Events(instr=PadSynth,
#             midinote=EventSeq(pad_midi_3),
#             beat=EventSeq(pad_beat, occurrences=inf), db=pad_db,
#             attack=0.1, decay=0.01, sustain=0.5, release=0.00001, bpm=171) \
#     .play()
#
# server.gui(locals(), exit=False)
# #server.start()
#
# while True:
#     pass



## import numpy as np
##
## sine_func       = lambda n, f=2:   np.sin(np.arange(n) * np.pi * 2 * f / float(n))
## sawtooth_func   = lambda n, f=2:   np.mod(np.arange(n) * 2.0 * f/n + f/2.0, 2) - 1
## square_func     = lambda n, f=2:   (sawtooth(f,n) >= 0) * 2.0 - 1
## def tri_func(n, f=2):
##     osc = 2 * sawtooth(f,n) * square(f,n) - 1
##     # This needs a phase shift on top:
##     sh = n / f / 4.0
##     return np.concatenate((osc[sh:], osc[:sh]))

# Define the sine function
# def sine_func(x, f):
#     return np.sin(x * np.pi * 2 * f)

# Define the sawtooth function
# def sawtooth_func(x, f):
#     return np.mod(x * 2.0 * f + f / 2.0, 2) - 1
#
# # Define the square function
# def square_func(x, f):
#     return np.where(x >= 0, 1.0, -1.0)
#
# # Define the tri function
# def tri_func(x, f):
#     osc = 2 * sawtooth_func(x, f) * square_func(x, f) - 1
#     sh = int(len(x) / f / 4.0)
#     return np.concatenate((osc[sh:], osc[:sh]))

# Create ufuncs from the functions using np.vectorize
# sine = np.vectorize(sine_func, excluded=['f'])
# sawtooth = np.vectorize(sawtooth_func, excluded=['f'])
# square = np.vectorize(square_func, excluded=['f'])
# tri = np.vectorize(tri_func, excluded=['f'])

## sine = np.frompyfunc(sine_func, 1, 1)
## sawtooth = np.frompyfunc(sawtooth_func, 1, 1)
## square = np.frompyfunc(square_func, 1, 1)
## tri = np.frompyfunc(tri_func, 1, 1)

# Test the ufuncs
## n = 1000  # Number of samples
## f = 5     # Frequency
##
## x = np.arange(n)
##
## sine_wave = sine(x, f=f)
## sawtooth_wave = sawtooth(x, f=f)
## square_wave = square(x, f=f)
## tri_wave = tri(x, f=f)
