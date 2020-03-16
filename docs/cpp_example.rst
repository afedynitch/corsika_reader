Reading CORSIKA Files in C++
-------------------------------

.. highlightlang:: cpp


One normally does not use the low-level interface in C++.
Inspecting a CORSIKA file using the high-level interface in C++::

    ShowerFile file(filename);
    corsika::Status status = file.FindEvent(1);

    cout << "Shower " << file.GetCurrentShower().GetShowerNumber() << ":\n"
         << "  primary: " << file.GetCurrentShower().GetPrimary() << "\n"
         << "  Energy:  " << file.GetCurrentShower().GetEnergy()/PeV << " PeV\n"
         << "  zenith:  " << file.GetCurrentShower().GetZenith()/deg << ", "
         << "  azimuth: " << file.GetCurrentShower().GetAzimuth()/deg << "\n"
         << "  N_muons: " << file.GetCurrentShower().GetMuonNumber() << endl;

    auto particles = file.GetCurrentShower().ParticleStream();
    while (auto it = particles.NextParticle()) {
         it != particles.end(); ++it) {
         ...
    }

More examples can be found in the examples directory.

