# Audacity Automation Script 
### Created as part of the Brainstorm project. 

Final script will automate the process of creating short audio clips.

## Instructions
1. Before running the script ensure audacity is open and has 'mod-script-pipe' enabled.
- Edit --> Preferences --> Modules --> mod-script-pipe 'Enabled'.

2. Ensure the relevant files to be merged are placed in the correct order within each input folder respectively. 
- **N.B.** Currently only supports .wav files

3. Edit main() on line(x) to include the arguments you want (see below) and run.

4. After the script has finished running the merged files and associated audacity projects will be visible in the relevant output folders.

**Ensure you re-open audicty if re-running the script. Failing to do so will cause exporting projects to fail!**

### Optional Arguments 
* *strip* - Removes any silence at the beginning & end of all tracks.
* *align* - Aligns the centre point of all tracks with the centrepoint of the longest track.
* *buffer* - Adds 1 second of silence before & after track plays.
* *white* - Adds low-volume white noise for the duration of the clip.
- For white noise longer than 3.5 seconds replace file in '/media'
* *exp_prj* - Also exports workspace as an audacity project & data file.

![Audacity Logo](https://www.audacityteam.org/wp-content/themes/wp_audacity/img/logo.png)

