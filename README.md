# GEM5-Systems
Analysis on Computer Organization using the GEM5 simulator
The [gem5 simulator](http://www.gem5.org/Main_Page) is a modular platform for computer-system architecture research, encompassing system-level architecture as well as processor microarchitecture.

The GEM5 simulator used for this project is current as of [May 15th, 2018](https://github.com/gem5/gem5/commit/ef96b32a28424e0d543198fee0964bb05c88704f)

With recent hardware security comprimises such as [*Spectre* and *Meltdown*](https://spectreattack.com), this repository serves to use GEM5 to build and test systems with the intent of 
* Reducing leakage [speculation](https://github.com/Eugnis/spectre-attack), or speculation footprints.
* Restricting side-channeling.
* Dynammic speculation throttling.

Current Agenda:

* Emulating a Intel Xeon core and running SPEC17 tests with variable system resources.
