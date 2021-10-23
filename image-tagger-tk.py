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
#image_file=Image.open('/darmok/data/tds-v0.0.2/dfb3983c260289ea.jpg')
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
#    annotate(str(array))

def load_next_sample(curr_image, image_file, anno, forward=True):
    index = tds_images.index(curr_image)
    breakout = False
    print(f'moving from {index}')
    if forward:
#        direction_modifier = 1
        if index == -1:
            print("END OF SET")
            breakout = True
        n_i = index + 1
    else:
#        direction_modifier = -1
        if index == 0:
            print("START OF SET")
            breakout = True
        n_i = index - 1
    print(f"shift from {index} to {n_i}.")
    anno_file_path = f"{tds_basepath}{tds_images[index][:-3]}txt"
    print(f"{anno_file_path}: {anno}")
    with open(anno_file_path, 'w') as f:
        f.write(str(anno))
    if breakout:
        return 0
    curr_anno_file = f"{tds_basepath}{tds_images[n_i][:-3]}txt"
#    anno = ""
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
#    image_file=Image.open('/darmok/data/tds-v0.0.2/0a110bca42890ac4.jpg')
    image=ImageTk.PhotoImage(image_file.resize((draw_width,draw_height)))
    label.configure(image=image)
    label.image = image
    root.bind('<space>', lambda event=None, curr_image=curr_image, image_file=image_file: load_next_sample(curr_image, image_file, anno))
    root.bind('<Shift-KeyPress-space>', lambda event=None, curr_image=curr_image, image_file=image_file, anno=anno: load_next_sample(curr_image, image_file, anno, False))
    print(f"{tds_basepath}{curr_image}: {draw_width}x{draw_height}")


def load_prev_sample(curr_image, image_file, anno):
    index = tds_images.index(curr_image)
    if index == 0:
        pass
    else:
        p_i = index-1
    print("doot doot from the prev_sample function")
    

def bind_nav(index, img_set):
    pass

#def annotate(annotation):
#    canvas.itemconfig(annotation_text,text=annotation)


root=Tk()

#canvas=Canvas(root)
#canvas.pack(fill='both',expand=True)
image=ImageTk.PhotoImage(image_file.resize((draw_width, draw_height)))
# image_portal = canvas.create_image(150,150,image=image)
# canvas.img_obj = image
# print(canvas.__dict__)
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
print(tds_buttons)
#button=Button(root,text='Annotate',command=annotate)
#button.pack()


root.mainloop()
