# Epic7 Infographic
(currently looking for a better, preferably punny or memey name)

This is a tool for turning builds within Epic7 into easy to share screenshots containing all relevant information. This tool HEAVILY relies on Fribbel's Epic 7 Optimizer, so [if you don't know what I'm talking about, check that out first!]((https://github.com/fribbels/Fribbels-Epic-7-Optimizer/)) 

Generally speaking, the goal of this tool is first to provide information, and then secondarily look good. I am not a graphics designer - so you may find it looks a bit boring - please give any suggestions for designs or feedback and I'll see what I can do. Currently it's setup in a super hacky way, but if there's interest I'd love to make it easier for people to make their own structures. 

Also, this work is almost entirely dependant on the work that Fribbels has done on their optimizer - and I want to give massive kudos and credit to them for their work. All the data, values, calculations and stat definitions from this come directly from their work, and all I've done is attach some image generation to it, so give them lots of kudos/support!

The remainder of the dependancies is on the [EpicSevenDB.com API](https://api.epicsevendb.com/) - which is where all the images and some other base stat information comes from. Super respect for having an open API that allows for projects like this to even exist. 


Example Infographic:
![](https://i.imgur.com/nVAVYtd.png)
_________________
## Requirements
- Windows PC (Created on Windows 10, untested on earlier versions)
- Installation of [Fribbel's Optimiser](https://github.com/fribbels/Fribbels-Epic-7-Optimizer/) with game data imported
_________________
# How to get it working
1. Copy artifactdata.json and herodata.json from within your Fribbels install into the same folder as the executable.  You can find them within data\cache in the Optimiser. These contain information about what heros and artifacts exist and where to find the right images.

2. Copy autosave.json from the FribbelsOptimizerSaves folder. This is the folder where you chose to save your builds in the client when installing. You can alternatively specifically save your current setup to a file by going to the Importer section of the optimiser and click Save Data, and name it autosave.json.

   The default folder is something similar to C:\Users\<username>\Documents\FribbelsOptimizerSaves
_________________
# How to actually make images:
## Command Line Config:
- Extract the files to a new directory
- [Open a command prompt](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/), then navigate to the directory you extracted the files to. (cd directorylocation)
- Run the executable and add the unit names after the executable names.  Make sure to use quotes for any character names with spaces. <screenshot>
  - For example: **e7-infographic "Seaside Bellona" Clarissa "General Purrgis" Sigret**

![](https://i.imgur.com/lfxygMo.png)

- Each unit will have an individual image stored in the output folder named after the character, and a multi-unit image in the output folder with the datetime after.

![](https://i.imgur.com/VhJ07aE.png)
_________________
## (Alpha) File Based Config:
- You can see an example of the file based variant in test_input.json / test_input2.json.
- Currently this file format is undocumented, but if you understand json data structures it's pretty easy to adjust and figure out.
- The advantages of these files is they let you configure the data beyond just deciding what units to use. It can configure the skill enhancement and artifact of the units, and in the future will include further customisation.
- To run a file based config run **e7-infographic file <filename.json>**
  - For example,  **e7-infographic file test_input.json**

![](https://i.imgur.com/PNMwTKz.png)

- The output image from the file based 

![](https://i.imgur.com/fzmwvMU.png)

_________________
## Known Issues:
- **General warning! This is a super early release, and was mostly cooked up quickly in a few days. Please be willing to accept some weirdness, bugs and ugliness for now.** It's unlikely this will do anything bad to your computer, but you may need to deal with a few problems to get it working.
- Some images will end up incorrectly aligned due to them appearing that way in the image sources used.
- Artifacts (and also therefore their stats) are not included in the data Fribbels captures - and so aren't generated with the standard command line method.
- Skill enhancements are not included in the data Fribbels captures - and so aren't generated with the standard command line method.

_________________
## Todo:
- Short term:
  - Refine file based definition and document it - hopefully adding more customisation in the process.
  - Add more customisation of attributes, especially derived values.
  - Fix a few bad alignments in the template
  - Making some of the logic less insane and dumb
- Long term:
  - Multiple output styles
