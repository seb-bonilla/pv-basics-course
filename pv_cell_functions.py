# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

"""Helper functions required by the silicon p–n junction solar-cell notebook."""

from devsim import (
    add_1d_contact,
    add_1d_mesh_line,
    add_1d_region,
    create_1d_mesh,
    create_device,
    delete_device,
    delete_mesh,
    finalize_mesh,
    get_contact_current,
    get_contact_list,
    get_device_list,
    get_mesh_list,
    set_node_values,
    set_parameter,
    solve,
)

from devsim.python_packages.model_create import CreateNodeModel, CreateSolution

from devsim.python_packages.simple_physics import (
    GetContactBiasName,
    SetSiliconParameters,
    CreateSiliconPotentialOnly,
    CreateSiliconPotentialOnlyContact,
    CreateSiliconDriftDiffusion,
    CreateSiliconDriftDiffusionAtContact,
)


def create_mesh(device, region):
    """Create the one-dimensional silicon device mesh used by the notebook."""
    create_1d_mesh(mesh="dio")
    add_1d_mesh_line(mesh="dio", pos=0, ps=1e-7, tag="top")
    add_1d_mesh_line(mesh="dio", pos=0.5e-5, ps=1e-9, tag="mid")
    add_1d_mesh_line(mesh="dio", pos=1e-5, ps=1e-7, tag="bot")
    add_1d_contact(mesh="dio", name="top", tag="top", material="metal")
    add_1d_contact(mesh="dio", name="bot", tag="bot", material="metal")
    add_1d_region(mesh="dio", material="Si", region=region, tag1="top", tag2="bot")
    finalize_mesh(mesh="dio")
    create_device(mesh="dio", device=device)


def set_parameters(device, region):
    """Set silicon material parameters at 300 K."""
    SetSiliconParameters(device, region, 300)


def set_net_doping(device, region):
    """Create the abrupt p–n net-doping profile."""
    CreateNodeModel(device, region, "Acceptors", "1.0e18*step(0.5e-5-x)")
    CreateNodeModel(device, region, "Donors", "1.0e18*step(x-0.5e-5)")
    CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")


def simulate_doped_silicon_bar(
    doping_values, voltages, length=0.1, width=1e-2, height=1e-2
):
    """Return I-V curves for a uniformly n-doped bar (dimensions in cm)."""
    curves = {}
    area = width * height

    for index, doping in enumerate(doping_values):
        device = f"SiliconBar{index}"
        mesh = f"bar_mesh{index}"
        region = "Silicon"

        if device in get_device_list():
            delete_device(device=device)
        if mesh in get_mesh_list():
            delete_mesh(mesh=mesh)

        create_1d_mesh(mesh=mesh)
        add_1d_mesh_line(mesh=mesh, pos=0, ps=length / 40, tag="left")
        add_1d_mesh_line(mesh=mesh, pos=length, ps=length / 40, tag="right")
        add_1d_contact(mesh=mesh, name="left", tag="left", material="metal")
        add_1d_contact(mesh=mesh, name="right", tag="right", material="metal")
        add_1d_region(mesh=mesh, material="Si", region=region, tag1="left", tag2="right")
        finalize_mesh(mesh=mesh)
        create_device(mesh=mesh, device=device)

        SetSiliconParameters(device, region, 300)
        set_parameter(device=device, region=region, name="taun", value=1e-6)
        set_parameter(device=device, region=region, name="taup", value=1e-6)
        CreateNodeModel(device, region, "Acceptors", "0")
        CreateNodeModel(device, region, "Donors", str(float(doping)))
        CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")

        initial_solution(device, region)
        solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=50)
        drift_diffusion_initial_solution(device, region)
        solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=50)

        left_bias = GetContactBiasName("left")
        right_bias = GetContactBiasName("right")
        set_parameter(device=device, name=right_bias, value=0.0)
        currents = []
        for voltage in voltages:
            set_parameter(device=device, name=left_bias, value=float(voltage))
            solve(type="dc", absolute_error=1e10, relative_error=1e-9, maximum_iterations=50)
            electron = get_contact_current(
                device=device, contact="left", equation="ElectronContinuityEquation"
            )
            hole = get_contact_current(
                device=device, contact="left", equation="HoleContinuityEquation"
            )
            currents.append((electron + hole) * area)

        curves[doping] = currents

    return curves


def display_silicon_bar(length, width, height, units="µm"):
    """Display a rotatable Plotly model of a rectangular silicon bar."""
    import plotly.graph_objects as go

    x = [0, length, length, 0, 0, length, length, 0]
    y = [0, 0, width, width, 0, 0, width, width]
    z = [0, 0, 0, 0, height, height, height, height]

    # Two triangles for each of the six faces.
    i = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
    j = [1, 2, 6, 7, 1, 5, 2, 6, 3, 7, 0, 4]
    k = [2, 3, 5, 6, 5, 4, 6, 5, 7, 6, 4, 7]

    fig = go.Figure(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            i=i,
            j=j,
            k=k,
            color="#87CEEB",
            opacity=0.85,
            flatshading=True,
            lighting=dict(ambient=0.55, diffuse=0.8, specular=0.25),
            hovertemplate=(
                f"Length: {length:g} {units}<br>"
                f"Width: {width:g} {units}<br>"
                f"Height: {height:g} {units}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title="Silicon bar (drag to rotate; scroll to zoom)",
        width=900,
        height=350,
        scene=dict(
            xaxis_title=f"Length ({units})",
            yaxis_title=f"Width ({units})",
            zaxis_title=f"Height ({units})",
            aspectmode="data",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.15)),
        ),
        margin=dict(l=5, r=5, b=5, t=30),
        showlegend=False,
    )
    fig.show()


def am15g_absorption_limit(bandgap_wavelength_nm, plot=True):
    """Plot AM1.5G and return ideal photon flux and current below a cutoff."""
    import matplotlib.pyplot as plt
    import numpy as np
    from pvlib import spectrum

    h = 6.62607015e-34       # Planck constant (J s)
    c = 299792458.0          # speed of light (m/s)
    q = 1.602176634e-19      # elementary charge (C)

    am15g = spectrum.get_reference_spectra(standard="ASTM G173-03")["global"]
    wavelength_nm = am15g.index.to_numpy(dtype=float)
    irradiance = am15g.to_numpy(dtype=float)  # W m^-2 nm^-1
    photon_energy = h * c / (wavelength_nm * 1e-9)
    photon_flux_spectrum = irradiance / photon_energy  # photons m^-2 s^-1 nm^-1
    absorbed = wavelength_nm <= bandgap_wavelength_nm

    photon_flux = np.trapz(
        photon_flux_spectrum[absorbed], wavelength_nm[absorbed]
    )
    current_density_mA_cm2 = q * photon_flux * 0.1
    bandgap_eV = 1239.841984 / bandgap_wavelength_nm

    if plot:
        plt.figure(figsize=(8, 4))
        plt.plot(wavelength_nm, irradiance, label="AM1.5G")
        plt.fill_between(
            wavelength_nm, 0, irradiance, where=absorbed, alpha=0.2,
            label="Photons with $E \\geq E_g$",
        )
        plt.axvline(
            bandgap_wavelength_nm, color="tab:red", linestyle="--",
            label=fr"$E_g={bandgap_eV:.2f}$ eV ({bandgap_wavelength_nm:g} nm)",
        )
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Spectral irradiance (W m$^{-2}$ nm$^{-1}$)")
        plt.title("ASTM G173-03 AM1.5G spectrum")
        plt.xlim(wavelength_nm.min(), wavelength_nm.max())
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return {
        "bandgap_eV": bandgap_eV,
        "photon_flux_m2_s": photon_flux,
        "maximum_current_density_mA_cm2": current_density_mA_cm2,
    }


def quasi_fermi_voltage(
    bandgap_eV,
    doping_cm3,
    excess_carriers_cm3,
    doping_type="n",
    temperature=300,
    plot=True,
):
    """Calculate and optionally plot Boltzmann quasi-Fermi levels."""
    import matplotlib.pyplot as plt
    import numpy as np

    k_eV = 8.617333262e-5
    thermal_energy = k_eV * temperature
    nc = 2.8e19   # silicon-like effective density of conduction states (cm^-3)
    nv = 1.04e19  # silicon-like effective density of valence states (cm^-3)
    intrinsic = np.sqrt(nc * nv) * np.exp(-bandgap_eV / (2 * thermal_energy))

    if doping_type.lower() == "n":
        electrons_dark = float(doping_cm3)
        holes_dark = intrinsic**2 / electrons_dark
    elif doping_type.lower() == "p":
        holes_dark = float(doping_cm3)
        electrons_dark = intrinsic**2 / holes_dark
    else:
        raise ValueError("doping_type must be 'n' or 'p'")

    electrons = electrons_dark + excess_carriers_cm3
    holes = holes_dark + excess_carriers_cm3

    valence_band = 0.0
    conduction_band = bandgap_eV
    intrinsic_level = bandgap_eV / 2 + 0.5 * thermal_energy * np.log(nv / nc)
    electron_qfl = intrinsic_level + thermal_energy * np.log(electrons / intrinsic)
    hole_qfl = intrinsic_level - thermal_energy * np.log(holes / intrinsic)
    qfl_separation = electron_qfl - hole_qfl

    if plot:
        plt.figure(figsize=(5, 5))
        plt.axhline(conduction_band, color="tab:blue", linewidth=3, label=r"$E_C$")
        plt.axhline(valence_band, color="tab:orange", linewidth=3, label=r"$E_V$")
        plt.axhline(
            electron_qfl, color="tab:green", linestyle="--", linewidth=2,
            label=r"$E_{Fn}$",
        )
        plt.axhline(
            hole_qfl, color="tab:red", linestyle="--", linewidth=2,
            label=r"$E_{Fp}$",
        )
        plt.annotate(
            "", xy=(0.72, electron_qfl), xytext=(0.72, hole_qfl),
            arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.5),
        )
        plt.text(
            0.75, 0.5 * (electron_qfl + hole_qfl),
            fr"$qV_{{oc,max}}$ = $\Delta E_F={qfl_separation:.2f}$ eV",
            va="center",
        )
        plt.xlim(0, 1.45)
        plt.ylim(-0.08 * bandgap_eV, 1.12 * bandgap_eV)
        plt.xticks([])
        plt.ylabel("Energy (eV)")
        plt.title("Quasi-Fermi-level splitting under illumination")
        plt.legend(loc="center left")
        plt.tight_layout()
        plt.show()

    return {
        "intrinsic_carrier_density_cm3": intrinsic,
        "electron_density_cm3": electrons,
        "hole_density_cm3": holes,
        "electron_quasi_fermi_eV": electron_qfl,
        "hole_quasi_fermi_eV": hole_qfl,
        "quasi_fermi_splitting_eV": qfl_separation,
        "maximum_voltage_V": qfl_separation,
    }


def initial_solution(device, region, circuit_contacts=None):
    """Set up the potential-only equilibrium problem and contact conditions."""
    CreateSolution(device, region, "Potential")
    CreateSiliconPotentialOnly(device, region)

    for contact in get_contact_list(device=device):
        if circuit_contacts and contact in circuit_contacts:
            CreateSiliconPotentialOnlyContact(device, region, contact, True)
        else:
            set_parameter(
                device=device,
                name=GetContactBiasName(contact),
                value=0.0,
            )
            CreateSiliconPotentialOnlyContact(device, region, contact)


def drift_diffusion_initial_solution(device, region, circuit_contacts=None):
    """Set up electron and hole drift–diffusion equations."""
    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")

    set_node_values(
        device=device,
        region=region,
        name="Electrons",
        init_from="IntrinsicElectrons",
    )
    set_node_values(
        device=device,
        region=region,
        name="Holes",
        init_from="IntrinsicHoles",
    )

    CreateSiliconDriftDiffusion(device, region)
    for contact in get_contact_list(device=device):
        if circuit_contacts and contact in circuit_contacts:
            CreateSiliconDriftDiffusionAtContact(device, region, contact, True)
        else:
            CreateSiliconDriftDiffusionAtContact(device, region, contact)


def simulate_complete_solar_cell(
    cell_width_um=100,
    p_doping_cm3=1e17,
    n_doping_cm3=1e15,
    tau_n_s=1e-3,
    tau_p_s=1e-3,
    generation_cm3_s=2.5e19,
    junction_fraction=0.5,
    cell_area_cm2=1.0,
    voltage_stop=0.8,
    voltage_step=0.02,
    temperature=300,
):
    """Run and plot a configurable illuminated 1D silicon solar cell."""
    import matplotlib.pyplot as plt
    import numpy as np

    device = "StudentSolarCell"
    mesh = "student_solar_mesh"
    region = "Silicon"
    q = 1.602176634e-19
    length_cm = cell_width_um * 1e-4
    junction_cm = junction_fraction * length_cm

    if not 0 < junction_fraction < 1:
        raise ValueError("junction_fraction must lie between 0 and 1")
    if device in get_device_list():
        delete_device(device=device)
    if mesh in get_mesh_list():
        delete_mesh(mesh=mesh)

    create_1d_mesh(mesh=mesh)
    add_1d_mesh_line(mesh=mesh, pos=0, ps=length_cm / 80, tag="top")
    add_1d_mesh_line(
        mesh=mesh, pos=junction_cm, ps=length_cm / 400, tag="junction"
    )
    add_1d_mesh_line(mesh=mesh, pos=length_cm, ps=length_cm / 80, tag="bot")
    add_1d_contact(mesh=mesh, name="top", tag="top", material="metal")
    add_1d_contact(mesh=mesh, name="bot", tag="bot", material="metal")
    add_1d_region(
        mesh=mesh, material="Si", region=region, tag1="top", tag2="bot"
    )
    finalize_mesh(mesh=mesh)
    create_device(mesh=mesh, device=device)

    SetSiliconParameters(device, region, temperature)
    set_parameter(device=device, region=region, name="taun", value=tau_n_s)
    set_parameter(device=device, region=region, name="taup", value=tau_p_s)
    CreateNodeModel(
        device, region, "Acceptors",
        f"{float(p_doping_cm3)}*step({junction_cm}-x)",
    )
    CreateNodeModel(
        device, region, "Donors",
        f"{float(n_doping_cm3)}*step(x-{junction_cm})",
    )
    CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")

    initial_solution(device, region)
    solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=80)
    drift_diffusion_initial_solution(device, region)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=80)

    # Retain SRH recombination and add uniform electron-hole photogeneration.
    CreateNodeModel(
        device, region, "ElectronGeneration",
        f"-{q}*USRH + {q}*{float(generation_cm3_s)}",
    )
    CreateNodeModel(
        device, region, "HoleGeneration",
        f"{q}*USRH - {q}*{float(generation_cm3_s)}",
    )

    top_bias = GetContactBiasName("top")
    bot_bias = GetContactBiasName("bot")
    set_parameter(device=device, name=bot_bias, value=0.0)
    voltages = np.arange(0, voltage_stop + 0.5 * voltage_step, voltage_step)
    current_density = []

    for voltage in voltages:
        set_parameter(device=device, name=top_bias, value=float(voltage))
        solve(
            type="dc", absolute_error=1e10, relative_error=1e-8,
            maximum_iterations=100,
        )
        electron = get_contact_current(
            device=device, contact="top", equation="ElectronContinuityEquation"
        )
        hole = get_contact_current(
            device=device, contact="top", equation="HoleContinuityEquation"
        )
        current_density.append(-(electron + hole))

    current_density = np.asarray(current_density)
    power_density = voltages * current_density
    positive_power = np.where(power_density > 0, power_density, 0)
    mpp_index = int(np.argmax(positive_power))
    jsc = float(current_density[0])
    vmpp = float(voltages[mpp_index])
    jmpp = float(current_density[mpp_index])
    pmpp = float(positive_power[mpp_index])

    crossings = np.where(np.diff(np.sign(current_density)) != 0)[0]
    if crossings.size:
        index = crossings[0]
        voc = float(np.interp(
            0.0,
            current_density[index:index + 2][::-1],
            voltages[index:index + 2][::-1],
        ))
    else:
        voc = np.nan

    fill_factor = pmpp / (voc * jsc) if voc > 0 and jsc > 0 else np.nan
    efficiency = 100 * pmpp / 0.1
    total_power_mw = 1e3 * pmpp * cell_area_cm2

    parameters = (
        f"Width={cell_width_um:g} µm | p={p_doping_cm3:.1e} cm⁻³ | "
        f"n={n_doping_cm3:.1e} cm⁻³ | τn={tau_n_s:.1e} s | "
        f"τp={tau_p_s:.1e} s | G={generation_cm3_s:.1e} cm⁻³ s⁻¹ | "
        f"area={cell_area_cm2:g} cm²"
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(voltages, 1e3 * current_density, "o-")
    axes[0].axhline(0, color="black", linewidth=0.8)
    axes[0].set(
        xlabel="Voltage (V)", ylabel="Current density (mA/cm²)",
        title="Illuminated J–V curve",
    )
    axes[0].grid(alpha=0.3)

    axes[1].plot(voltages, 1e3 * power_density, "o-", color="tab:orange")
    axes[1].plot(vmpp, 1e3 * pmpp, "ro", label=f"MPP = {1e3 * pmpp:.2f} mW/cm²")
    axes[1].set(
        xlabel="Voltage (V)", ylabel="Power density (mW/cm²)",
        title="Power–voltage curve",
    )
    axes[1].grid(alpha=0.3)
    axes[1].legend()
    fig.suptitle(parameters, fontsize=10)
    fig.tight_layout()
    plt.show()

    print(f"Jsc = {1e3 * jsc:.2f} mA/cm²")
    print(f"Voc = {voc:.3f} V")
    print(f"Maximum power density = {1e3 * pmpp:.2f} mW/cm²")
    print(f"Total maximum power = {total_power_mw:.2f} mW")
    print(f"Fill factor = {fill_factor:.3f}")
    print(f"Efficiency = {efficiency:.2f} %")

    return {
        "voltage_V": voltages,
        "current_density_A_cm2": current_density,
        "power_density_W_cm2": power_density,
        "Jsc_A_cm2": jsc,
        "Voc_V": voc,
        "Vmpp_V": vmpp,
        "Jmpp_A_cm2": jmpp,
        "Pmpp_W_cm2": pmpp,
        "total_power_W": pmpp * cell_area_cm2,
        "fill_factor": fill_factor,
        "efficiency_percent": efficiency,
    }
