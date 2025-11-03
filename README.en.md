[English](./README.en.md) | **中文**

<h1>WeChat Robot Packaging (Encrypted)</h1>
<ol>
<li>This project is for educational and research purposes only and is no longer maintained. Please comply with the GPL 3.0 license.</li>
<li>It is a secondary wrapper based on the pywin32 library, combined with the easyocr library to realize basic key-ghost operations. Required packages: pywin32, easyocr.</li>
<li>The main program is located in StarRailAutoClass.py and can be switched to run in the background.</li>
<li>For study only, using the first-version key-wrapper which is imperfect—please don’t mind.</li>
</ol>

<h2>Additional Notes:</h2>
<ol>
<li>Display scaling <strong>must</strong> be manually set to 100 %. Remember the original value.  
Resolution will be auto-adjusted by the script at start and restored at end.  
How-to: right-click desktop → “Display settings”; or press Win key and search “resolution” → “Change resolution”, then set scale to 100 %.</li>

<li>In-game resolution should be the highest available (2560 × 1440 or larger). Turn on “Auto-Battle” in game.</li>

<li>The game <strong>cannot run in the background</strong>; keep its window visible.</li>

<li>You can either:<br>
 – manually launch the game and then start the script, or<br>
 – provide the <strong>absolute path</strong> of the game exe; the script will launch the game for you.<br>
When the script finishes, the game will be closed automatically and a pop-up will show you the “Daily task completion status”.</li>
</ol>

<h2>Good to Know:</h2>
<ol>
<li>Code for “Simulated Universe farming” already exists but is disabled because it is unstable.</li>

<li>The built-in Key-ghost tool shows ads; the script removes them at start-up, but this is not 100 % reliable. Suggested workflow: disconnect network → launch → reconnect.</li>

<li>The script encapsulates common mouse-click functions, keyboard-click functions, screen-resolution conversion functions, etc.</li>

<li>Currently called modules: dungeon farming, synthesis, material exploration, daily claim, guide teleport, plus a bunch of nested sub-functions. For efficiency only one worker thread is started.</li>

<li>All coordinates depend on screen resolution and scaling. Resolution can be changed in code, but scaling cannot; therefore <strong>scaling = 100 % is mandatory</strong>.</li>

<li>Default reference: 1920 × 1080, 100 % scaling. If yours differs, modify the settings (Win → search “resolution”). Remember your original scaling value so you can restore it later. The script will temporarily switch to the reference resolution and restore it after execution. “Initial system standard values are for coordinate alignment; offset will not be large.”</li>
</ol>

Final disclaimer:  
The script already contains “triple anti-ban + double anti-detection” code and has been tested for 3 months without issues, but **no 100 % safety is guaranteed**—use at your own risk.  
(If you are still worried, charging a small monthly card gives 99.9 % safety; currently 99 %.)  
The script embeds a watermark for anti-theft; **do not resell or redistribute lightly**.  
I made this just to auto-farm until my Star Rail wife is max-constellation.  
**Tech otakus save the world!**