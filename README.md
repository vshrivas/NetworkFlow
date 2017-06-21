# graphospasm
A graph DB that writes so fast, you'll get writer's cramp.

## Setup
First, you need to make sure Python 3 is installed. Try this:
```bash
python3 --version
```
If you see something like `Python 3.5.2`, great; move on to the next step. If you get `python3: command not found`, you need to install it. Run
```bash
sudo apt-get install python3
```
and let it install. Next, you need `python3-pip` in order to get ANTLR4 working properly. Run
```bash
pip3 --version
```
and see if it works. If it does not, just run
```bash
sudo apt-get install python3-pip
```
and let it do its thing. Now, try the following two lines to see if you have the Python module `setuptools`:
```bash
python3 -c "import setuptools"
echo $?
```
If `0` is printed to the command-line, move on. If not, you need to install setuptools via
```bash
pip3 install setuptools
```
Finally, we need ANTLR4 to work. Try this:
```bash
python3 -c "import antlr4"
echo $?
```
If you get `0`, you're done! If not, just run
```
pip3 install antlr4-python3-runtime
```
to finish setup. Now, you should be able to run graphospasm just by invoking the following command from the top-level directory:
```bash
python3 graphospasm.py
```
If it doesn't work, try installing any missing modules via `pip3`. If that doesn't work, let us know via Github or otherwise!
