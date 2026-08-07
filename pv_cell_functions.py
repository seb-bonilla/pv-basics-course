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
