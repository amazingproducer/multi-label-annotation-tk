from tkinter import *
from PIL import Image,ImageTk
import os
import json


tds_basepath = "/darmok/data/tds-v0.0.2/"
tds_files = os.listdir(tds_basepath)
tds_labels = ["vehicle", "person", "tundra-parked"]
tds_images = []
for i in tds_files:
    if i.endswith('.jpg'):
        tds_images.append(i)


draw_width = 640
curr_image = tds_images[0]
image_file=Image.open(f'{tds_basepath}{curr_image}')
image_width, image_height = image_file.size
print(f"Image dimensions: {image_width},{image_height}")
draw_height = int(draw_width * image_height / image_width)
print(f"Drawn dimensions: {draw_width}x{draw_height}")

def create_annotation():
    anno_array = []
    for i in tds_labels:
        anno_array.append(0)
    return anno_array


def modify_annotation(label, array):
    bit = array[tds_labels.index(label)]
    if bit == 1:
      array[tds_labels.index(label)] = 0
      tds_buttons[label].config(relief="raise")
    else:
      array[tds_labels.index(label)] = 1
      tds_buttons[label].config(relief="sunken")
    print(label, array)
    annotation_text.delete('1.0', END)
    annotation_text.insert(END, str(array))

def load_next_sample(curr_image, image_file, anno, forward=True, ignore_existing=False):
    index = tds_images.index(curr_image)
    breakout = False
    print(f'moving from {index}')
    n_i = 0
    if forward:
#        direction_modifier = 1
        if tds_images[index] == tds_images[-1]:
            print("END OF SET")
            breakout = True
        n_i = index + 1
    else:
#        direction_modifier = -1
        if index == 0:
            print("START OF SET")
            breakout = True
        n_i = index - 1
    if ignore_existing:
        anno_list = []
        for i in os.listdir(tds_basepath):
            if i.endswith('.txt'):
                anno_list.append(i)
        print(f"Found {len(anno_list)} annotations.")
        for i in range(len(tds_images)):
            checkpath = f"{tds_images[i][:-3]}txt"
            print(f"looking for{checkpath}")
            if checkpath not in anno_list:
                n_i = i
                break
    print(f"shift from {index} to {n_i}.")
    anno_file_path = f"{tds_basepath}{tds_images[index][:-3]}txt"
    print(f"{anno_file_path}: {anno}")
    with open(anno_file_path, 'w') as f:
        f.write(str(anno))
    if breakout:
        return 0
    curr_anno_file = f"{tds_basepath}{tds_images[n_i][:-3]}txt"
    fileopen_mode = 'r' if os.path.exists(curr_anno_file) else 'w+'
    with open(curr_anno_file, fileopen_mode) as f:
        print(fileopen_mode)
        checkval = f.read()
        print(checkval)
        if checkval:
            anno = json.loads(checkval)
        else:
            anno = [0,0,0]
            f.write("[0,0,0]")
    annotation_text.delete('1.0', END)
    annotation_text.insert(END, str(anno))
    for i in tds_labels:
        tds_buttons[i].pack_forget()
        tds_buttons[i] = Button(root,text=i,command=lambda i=i, anno=anno: modify_annotation(i, anno))
        tds_buttons[i].pack(fill='both', expand=True)
        tds_key_str = i[0]
        root.bind(tds_key_str, lambda event=i, i=i, anno=anno: modify_annotation(i, anno))
        if anno[tds_labels.index(i)] == 0:
            tds_buttons[i].config(relief='raise')
        else:
            tds_buttons[i].config(relief='sunken')
    curr_image = tds_images[n_i]
    image_width, image_height = image_file.size
    draw_height = int(draw_width * image_height / image_width)
    image_file=Image.open(f'{tds_basepath}{curr_image}')
    image=ImageTk.PhotoImage(image_file.resize((draw_width,draw_height)))
    label.configure(image=image)
    label.image = image
    root.bind('<space>', lambda event=None, curr_image=curr_image, image_file=image_file: load_next_sample(curr_image, image_file, anno))
    root.bind('<Shift-KeyPress-space>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno, forward=False))
    root.bind('<End>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno, ignore_existing=True))
    print(f"{tds_basepath}{curr_image}: {draw_width}x{draw_height}")

root=Tk()

image=ImageTk.PhotoImage(image_file.resize((draw_width, draw_height)))
label = Label(image=image)
label.image = image
label.pack()
anno = create_annotation()
annotation_text=Text(root, width=45, height=1)
annotation_text.pack()
anno_file = f"{tds_basepath}{tds_images[0][:-3]}txt"
print(f"opening annotation file: {anno_file}")
fileopen_mode = 'r' if os.path.exists(anno_file) else 'w+'
with open(anno_file, fileopen_mode) as f:
    print(fileopen_mode)
    checkval = f.read()
    print(checkval)
    if checkval:
        anno = json.loads(checkval)
    else:
        anno = [0,0,0]
        f.write("[0,0,0]")


annotation_text.delete('1.0', END)
print(type(annotation_text))
annotation_text.insert(END, str(anno))
tds_buttons = {}
for i in tds_labels:
    tds_buttons[i] = Button(root,text=i,command=lambda i=i, anno=anno: modify_annotation(i, anno))
    tds_buttons[i].pack(fill='both', expand=True)
    tds_key_str = i[0]
    root.bind(tds_key_str, lambda event=i, i=i, anno=anno: modify_annotation(i, anno))

root.bind('<space>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno))
root.bind('<Shift-KeyPress-space>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno, False))
root.bind('<End>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno, ignore_existing=True))
print(tds_buttons)

root.mainloop()
