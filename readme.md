# Axe Controlled Minecraft

## How to use
- Run `python list_device.py` to get list of all your audio device. Remember the ID which your preferred audio belong to.
- In `graph.py` line 53, change `input_device_index` to the ID of your audio device. Example: `input_device_index=2`
- Run `python graph.py`, then start making noise with your axe. From there, you should find the treshold of your axe sound. 
- In `main.py`, change `THRESHOLD` value.
- Final part... `python main.py` 