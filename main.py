def generate_brocade_config(input_data):
    # Split input into separate lines
    lines = input_data.split("\n")

    # Initialize variables
    brocade_cmds = []
    zone_name = ""
    members = []
    fcaliases = []
    zones = []

    # Parse input and generate Brocade commands
    for line in lines:
        words = line.split()

        if "zoneset name" in line:
            # Extract zone set name and VSAN
            zone_set_name = words[2]

        elif "zone name" in line:
            # Extract zone name
            zone_name = words[2]
            zones.append(zone_name)
            # Append command to create zone
            brocade_cmds.append(f"zonecreate '{zone_name}'")

        elif "member" in line:
            # Extract member PWWN and append to members list
            member_pwwn = words[2]
            members.append(member_pwwn)
            # Append command to add member to zone
            brocade_cmds.append(f"zoneadd '{zone_name}', '{'alias_'+member_pwwn}'")

        elif "zoneset activate" in line:
            # Extract zone set name and VSAN
            zone_set_name = words[2]
            vsan = words[4]

            # Append command to activate zone set
            brocade_cmds.append(f"zoneset activate {zone_set_name} vsan {vsan}")

            # Append command to upload config
            brocade_cmds.append("configupload -p /fabric/zone > myzones.txt")
    if members:
        # Create aliases for members
        for pwwn in members:
            fcaliases.append('alicreate \'alias_' + pwwn + '\',\'' + pwwn + '\'')
        for fcalias in fcaliases:
            brocade_cmds.insert(0,fcalias)
    if zone_set_name:
        # Create a configuration
        brocade_cmds.append(f"cfgcreate '{zone_set_name}'")
        # Append commands to add zones to the configuration
        for zone in zones:
            brocade_cmds.append('cfgadd \'' + zone_set_name + '\',\'' + zone + '\'')
        # Append commands to save and enable the configuration
        brocade_cmds.append(f"cfgsave")
        brocade_cmds.append(f"cfgenable '{zone_set_name}'")

    return "\n".join(brocade_cmds)


def main():
    input_data = """
    zoneset name myzoneset vsan 10
        zone name myzone1 vsan 10
            member pwwn 10:00:00:00:00:00:00:01
            member pwwn 10:00:00:00:00:00:00:02
        zone name myzone2 vsan 10
            member pwwn 10:00:00:00:00:00:00:03
            member pwwn 10:00:00:00:00:00:00:04
    """

    output_data = generate_brocade_config(input_data)
    print(output_data)


if __name__ == "__main__":
    main()
