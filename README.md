<html>
<body>
<!--StartFragment--><html><head></head><body><h1>CaveDuster 💣</h1>
<p>A minesweeper-inspired game built in Python with Pygame, made as a fun project to explore and implement classic algorithms hands-on.</p>
<h2>Algorithms &amp; Design</h2>
<p>The interesting parts under the hood:</p>
<ul>
<li><strong>Recursive flood-fill</strong> — when you reveal a cell with no adjacent mines, it recursively uncovers all neighboring empty cells, chaining outward until it hits numbered boundary cells. Same idea as a paint bucket tool.</li>
<li><strong>BFS-style neighbor exploration</strong> — cell weights (the numbers) are computed by walking all 8 neighbors of every non-mine cell and counting adjacent mines.</li>
<li><strong>Deferred mine placement</strong> — mines aren't placed at game start. They're placed on your <em>first click</em>, guaranteeing you can never lose immediately. The clicked cell is always excluded from mine placement.</li>
<li><strong>Shuffle queue</strong> — the music player uses a proper shuffle queue rather than picking randomly each time, so every track plays once before anything repeats.</li>
</ul>
<h2>Features</h2>
<ul>
<li>🎮 Mouse and controller support (tested on PXN Switch controller)</li>
<li>🚩 Left click to reveal, right click to flag</li>
<li>🎵 Sidebar music player with play/pause, prev/next, shuffle, and volume control</li>
<li>⏱ HUD with live mine counter and timer</li>
<li>🔄 Press <code>R</code> to restart at any time</li>
</ul>
<h2>Setup</h2>
<p><strong>Requirements</strong></p>
<pre><code>pip install pygame
</code></pre>
<p><strong>Music</strong></p>
<p>Create a <code>music/</code> folder in the project root and drop any <code>.mp3</code>, <code>.wav</code>, or <code>.ogg</code> files into it. The game will load them all automatically as a playlist.</p>
<pre><code>CaveDuster/
├── music/        ← put your songs here
├── cave_duster_driver.py
├── mineGrid.py
├── cell.py
└── README.md
</code></pre>
<p><strong>Run</strong></p>
<pre><code>python main.py
</code></pre>
<h2>Controls</h2>

Input | Action
-- | --
Left click | Reveal cell
Right click | Flag / unflag cell
R | Restart
Escape | Quit
D-pad | Move cursor
A button | Reveal cell
B button | Flag cell
Start button | Restart

</body></html><!--EndFragment-->
</body>
</html>
