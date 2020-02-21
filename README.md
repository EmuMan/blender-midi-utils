# MIDI Utils for Blender

## A Blender addon to facilitate the conversion of MIDI into 3D animation

___

MIDI Utils is an addon on Blender to add all-around support for MIDI-driven animation in Blender. I've wanted something like this ever since I saw [ANIMUSIC](https://www.animusic.com/)'s stuff, but I couldn't really find anything online on how to actually do it, especially specifically for Blender. There are a few other solutions available online, but I couldn't find an easy to use, comprehensive addon for it, so I decided to make one.

## Installation

___

Before you install MIDI Utils, you need to install Mido, a Python library for MIDI, through PIP, Python's package installer. Since Blender uses its own version of Python, it needs to be installed in a special manner. Open a command prompt and type in `cd C:\Program Files\Blender Foundation\Blender\2.80\python\bin`, replacing the path with the correct one for your OS/installation if it's different. Then, run `python.exe -m pip install mido`, or `./python -m pip install mido` if you're on Linux/MacOS (not tested but should work?). The installation should complete without any errors.

Installing MIDI Utils is easy. Simply click the green "Clone or download" button and then the "Download ZIP" button that comes up. You can then go into Blender and install the addon by following Edit -> Preferences -> Addons -> Install. Navigate to wherever the ZIP file downloaded and install it. It should pop up as an addon, where you can tick the box to enable it. You'll find the panel under a tab called "MIDI Utils" in the 3D viewport when you hit "N".

## Capabilities

___

MIDI Utils is still very much experimental at this point. It only supports the creation of position and rotation keyframes, as well as keyboard setups. More features will very likely be added in the future.

## The Panel

___

### General

* **MIDI File** - The MIDI file to sync keyframes to
* **Track** - The track of the MIDI file to pull messages from (if you don't know, just leave at 1 and it will probably work)

### Keyframes

* **Keyframe type** - The type of keyframe to apply (currently only rotation or position)
* **Keyboard (location only)** - The keyboard to use when determining locations (see Keyboards section below)
* **Rest position/location** - The position/location of the object when at rest
* **Strike position/location** - The position/location of the object when striking a note
* **Anticipation** - How much the movement is anticipated, such as a mallet moving up slightly before actually striking the note. Interpolated backwards from the given rest/strike values.
* **Attack time** - The amount of time it takes to strike
* **Release time** - The amount of time it takes to release
* **Delay** - The amount of time to wait before starting the animation.
* **Create Keyframes** - Use the given inputs to create new keyframes

### Create Keyboard

* **Collection name** - What to name the keyboard collection
* **Start note** - The note the keyboard starts on (C0 = 0)
* **Length** - The length of the keyboard
* **Key displacements**
  * **X** - The distance in between each key. Black keys are placed in between white keys, meaning 1/2 the displacement.
  * **Y** - The Y displacement in between white and black keys
  * **Z** - The Z displacement in between white and black keys
* **Linear** - When enabled all of the keys are lined up rather than arranged in a typical piano fashion and Y/Z displacements are ignored
* **Create Keyboard** - Use the given inputs to create a new keyboard

## Keyboards

___

Keyboards are an important but slightly complicated part of this addon so they deserve their own section. Each keyboard is defined by a normal collection, and within each collection there are empties (or any other object) that are used as keys. These keys follow a very specific naming convention: `<collectionname>_<notename>`. For example, note 63 within a keyboard collection named Keys would be represented by an empty named Keys_63. It's important to note that creating a keyboard with the same name as another keyboard will break things and you might have to go into the outliner and delete things. When location keyframes are generated, if a keyboard collection is specified (name must be exact and cased correctly), the object will follow the keyboard empties and jump to whichever one is associated with the current MIDI note. If a key is not found, it will default to its origin (see below). You can move these empties however you like, and you can even make your own keyboard collections as long as they follow the correct naming conventions.

## Other Things to Note

___

* Location keyframes are relative to wherever the object starts. When keyframes are generated, the origin of each of the locations is set to the original location of the object, meaning that if the object starts at `z=5` and the specified rest position is at `z=1`, then the actual rest position in world space is at `z=6`.
* Rotation keyframes are defined in world space, meaning that if you specify a rest rotation of 10 degrees the rest rotation will be 10 degrees no matter the starting rotation when the keyframes are applied.
