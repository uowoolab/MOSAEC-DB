using CrystalNets

function main(args)
        show(determine_topology_dataset(args, true, true, true, CrystalNets.Options(export_subnets=false, export_net=false, export_clusters=false, export_input=false, export_trimmed=false, structure=StructureType.MOF, bonding=Bonding.Input, detect_organiccycles=false, clusterings=[Clustering.Auto, Clustering.Standard])))
end

main(ARGS[1])

