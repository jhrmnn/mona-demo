This is a demo project for the calculation framework [Mona](https://github.com/azag0/mona).

### Prerequisites

In `PATH`:

- `mona_aims`: Runs FHI-aims, the executable may be specified by the `MONA_AIMS` environment variable.
- `aims-mona-demo`: FHI-aims executable, version 181110.

Environment variables:

- `AIMS_SPECIES_DEFAULTS` points to the `species_defaults` directory.

### Instructions

```
git clone https://github.com/azag0/mona-demo.git
cd mona-demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export MONA_APP=mona_demo:app
mona init
make
```
