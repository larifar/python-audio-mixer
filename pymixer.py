import tkinter as tk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class AudioControlApp:
    def __init__(self, master):
        self.master = master
        master.title("Controle de Áudio")

        self.volume_label = tk.Label(master, text="Volume:")
        self.volume_label.pack()

        self.volume_scale_left = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume_left)
        self.volume_scale_left.set(self.get_volume_left())
        self.volume_scale_left.pack()

        self.volume_scale_right = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume_right)
        self.volume_scale_right.set(self.get_volume_right())
        self.volume_scale_right.pack()

        self.mute_right_button = tk.Button(master, text=self.change_text(not self.is_muted(1)) +" RIGHT",
                                           command=self.toggle_mute_right)
        self.mute_right_button.pack()

        self.mute_left_button = tk.Button(master, text=self.change_text(not self.is_muted(0)) +" LEFT",
                                          command=self.toggle_mute_left)
        self.mute_left_button.pack()

        self.mute_both_button = tk.Button(master, text=self.change_text(not self.get_speakers().GetMute()) +" BOTH",
                                          command=self.toggle_mute_both)
        self.mute_both_button.pack()

        self.previous_volume_left = self.get_volume_left()
        self.previous_volume_right = self.get_volume_right()

    def get_speakers(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return volume

    def set_channel_volume(self, channel, value):
        volume = self.get_speakers()
        volume.SetChannelVolumeLevelScalar(channel, float(value) / 100.0, None)

    def set_volume_left(self, value):
        self.set_channel_volume(0, float(value))

    def get_volume_left(self):
        volume = self.get_speakers()
        return int(volume.GetChannelVolumeLevelScalar(0) * 100)

    def set_volume_right(self, value):
        self.set_channel_volume(1, float(value))

    def get_volume_right(self):
        volume = self.get_speakers()
        return int(volume.GetChannelVolumeLevelScalar(1) * 100)

    def is_muted(self, channel):
        volume = self.get_speakers().GetChannelVolumeLevelScalar(channel)
        return volume == 0

    def toggle_mute_left(self):
        current_mute = self.is_muted(0)
        if (current_mute):
            self.set_channel_volume(0, self.previous_volume_left)
            self.mute_left_button["text"] = self.change_text(current_mute) + " LEFT"
        else:
            self.previous_volume_left = self.get_volume_left()
            self.set_channel_volume(0, 0)
            self.mute_left_button["text"] = self.change_text(current_mute) + " LEFT"


    def toggle_mute_right(self):
        current_mute = self.is_muted(1)
        if (current_mute):
            self.set_channel_volume(1, self.previous_volume_right)
            self.mute_right_button["text"] = self.change_text(current_mute) + " RIGHT"
        else:
            self.previous_volume_right = self.get_volume_right()
            self.set_channel_volume(1, 0)
            self.mute_right_button["text"] = self.change_text(current_mute) + " RIGHT"


    def toggle_mute_both(self):
        volume = self.get_speakers()
        current_mute = volume.GetMute()
        volume.SetMute(not current_mute, None)
        self.mute_both_button["text"] = self.change_text(current_mute) + " BOTH"
        self.mute_right_button["text"] = self.change_text(current_mute) + " RIGHT"
        self.mute_left_button["text"] = self.change_text(current_mute) + " LEFT"

    def set_mute(self, channel):
        self.set_channel_volume(channel, 0)

    def change_text(self, value):
        return "Mute" if value else "Unmute"



if __name__ == "__main__":
    root = tk.Tk()
    app = AudioControlApp(root)
    root.mainloop()



