# Braitenberg Vehicles (pygame)

Small simulations of [Braitenberg vehicles](https://en.wikipedia.org/wiki/Braitenberg_vehicle): simple agents whose sensors are wired directly to their motors, producing light-seeking or light-avoiding behaviour without any "planning". Built as lab exercises in Python with `pygame`.

| File | What it shows |
|---|---|
| `vehicle_01_light_follower.py` | One vehicle with a single sensor that turns towards a "sun" (follows the mouse cursor) and slows down as it gets close. |
| `vehicle_02a_stereo_sensors.py` | Two sensors, each driving the motor on its own side. Speed and turning come from inverse-distance light intensity. Commented-out variants cover crossed wiring and sensors placed behind the vehicle. |
| `vehicle_02b_swarm_collisions.py` | A swarm of 20 vehicles with crossed sensor-motor wiring around a central sun; vehicles bounce off each other with random jitter on collision. |
| `vehicle_03_inhibitory_mono_stereo.py` | Vehicles 3A/3B: inhibitory wiring, mono vs. stereo sensing, crossed wiring, three activation functions (inverse distance, threshold, sine) and optional motor noise. Keys: `M` toggles mono/stereo, `N` toggles noise. |

## Run

```bash
pip install -r requirements.txt
python vehicle_03_inhibitory_mono_stereo.py
```

Close the window to quit.

## Notes

- Written for a university course on embodied/cognitive modelling. Parameters (speeds, turn rates, scaling) are hand-tuned, not fitted.
