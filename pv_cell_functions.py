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
    finalize_mesh,
    get_contact_list,
    set_node_values,
    set_parameter,
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
