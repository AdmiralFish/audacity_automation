# Audacity Automation Script 
## Created as part of the Brainstorm project. 

Final script will automate the process of creating short audio clips.

### Instructions

**Ensure you re-open audicty if re-running the script. Failing to do so will cause exporting projects to fail!**

Before running the script ensure audacity is open and has 'mod-script-pipe' enabled.
- Edit --> Preferences --> Modules --> mod-script-pipe 'Enabled'.

Also ensure the relevant files to be merged are placed in the correct order within the 'set_a' and 'set_b' folders respectively. 

After the script has finished running the merged files and associated audacity projects will be visible in the exported_files and exported_projects folders.


### Task list 

- [x] Initatie pipeline to Audacity 
- [X] Import track1 and track2
- [X] Automate importing from directory
- [x] Pull track info into Python 
- [ ] Output track length to external file 
- [X] Trim whitespace from either side (silence)
- [x] Normalize duration for both tracks 
- [x] Add standard amount of silence to both ends
- [X] Export as MP3 / WAV
- [X] OPTIONAL - Save audacity project 
- [X] Reset workspace

![Audacity Logo](https://www.audacityteam.org/wp-content/themes/wp_audacity/img/logo.png)

