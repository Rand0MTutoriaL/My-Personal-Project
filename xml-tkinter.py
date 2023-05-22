import tkinter as tk
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET
from lxml import etree
from time import sleep


def win_center_pos(window, win_size):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    pos = (int((screen_width/2) - (win_size[0]/2)), int((screen_height/2) - (win_size[1]/2)))
    return pos


def sizing_positioning(size, pos):
    return f"{size[0]}x{size[1]}+{pos[0]}+{pos[1]}"


class MainWindow:
    def __init__(self, window_size=None, original=True):
        self.window = Tk()
        if not original:
            self.window_size = window_size
            self.position = win_center_pos(self.window, self.window_size)
        self.Components = {}

    def initiate_window_launch(self, title=None, resizable_tuple=None):
        self.window.title(title)
        self.window.resizable(resizable_tuple[0], resizable_tuple[1])
        if self.position and self.window is not None:
            self.window.geometry(sizing_positioning(self.window_size, self.position))

    def create_component(self, xml_component_list):
        root_components = etree.fromstring(xml_component_list)
        all_elem_components = root_components.iterdescendants()
        for component in all_elem_components:
            if component.get('type', default=None) == "text":
                font_tuple = (component.get('font', default='TkDefaultFont'), component.get('font-size', default=10))
                self.Components.update({component.tag:
                {
                    "Parent": component.getparent().tag,
                    "Object": Label(
                        self.window,
                        text=component.text,
                        font=font_tuple
                        # More soon
                    )
                }})
            else:
                pass
                # More soon
        print(self.Components)
        # return self.ComponentsTxt

    def update_page(self, xml_update_components):
        updating_components = etree.fromstring(xml_update_components)
        all_updating_elem_components = updating_components.iterdescendants()
        for key, former_component, updates in zip(self.Components.keys(), self.Components.values(), all_updating_elem_components):
            if key == updates.tag:
                former_component["Object"].config(text=updates.text)

    def position_component(self, xml_packing):
        positions_root = etree.fromstring(xml_packing)
        positions_list = positions_root.iterdescendants()
        for key, component, position in zip(self.Components.keys(), self.Components.values(), positions_list):
            if key == position.tag:
                if position.get('method') == "pack":
                    component["Object"].pack(ipady=position.get('ipady', default=None))
                elif position.get('method') == "grid":
                    pass
                else:
                    pass

    def complete_setup(self):
        self.window.mainloop()


win = MainWindow(window_size=(500, 500), original=False)
win.initiate_window_launch(title="test", resizable_tuple=(FALSE, FALSE))
win.create_component(
    '''
        <rootComponents>
            <Text type="text">porewwre</Text>
            <Parent>
                <Child type="text">eee</Child>
            </Parent>
        </rootComponents>
    '''
)
win.position_component(
    '''
        <ComponentsPositions>
            <Text method="pack" ipady="5" />
            <Child method="pack" ipady="10" />
        </ComponentsPositions>
    '''
)
win.update_page(
    '''
        <UpdatesComponents>
            <Text>hhah</Text>
        </UpdatesComponents>
    '''
)

win.complete_setup()
