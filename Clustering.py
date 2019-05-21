import bpy
from sklearn.cluster import DBSCAN, OPTICS

bl_info = {
    "name": "Clustering",
    "author": "Henri Hakala, Joel Pesu (Wakeone)",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "description": "Runs a clustering algorithm on the selected objects.",
    "category": "Object",
}

clustering_algorithm = [
    'DBSCAN',
    'OPTICS',
]

def Fit(context, positions):
    if context.scene.clustering_group.Mode == 'DBSCAN':
        return DBSCAN(eps=context.scene.clustering_group.Eps, min_samples=context.scene.clustering_group.MinSamples).fit(positions)
    elif context.scene.clustering_group.Mode == 'OPTICS':
        return OPTICS(min_samples=context.scene.clustering_group.MinSamples, xi=context.scene.clustering_group.Xi).fit(positions)
    else:
        print("Unsupported clustering mode.")
        return None

def ProcessClustering(self, context):

    if not context.scene.clustering_group.SelectedOnly:
        bpy.ops.object.select_all(action='SELECT')

    # Preprocess the model
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.visual_transform_apply()
    bpy.ops.object.make_single_user(type='ALL', object=True, obdata=True, material=False, animation=False)

    print("Processing clusters...")

    # Split the objects by material if needed.
    objects_to_cluster = {}
    if context.scene.clustering_group.ByMaterial:
        objects_to_cluster = SplitByMaterial(bpy.context.selected_objects)
    else:
        objects_to_cluster["Default"] = bpy.context.selected_objects

    processed_clusters = {}
    for material, objcluster in objects_to_cluster.items():
        positions = [obj.location for obj in objcluster]

        # If we there are less objects in the cluster than min_samples just treat them as a cluster.
        if len(positions) < context.scene.clustering_group.MinSamples: 
            x = {}
            x['0'] = objcluster
            processed_clusters[material] = x
            continue
        else:
            db = Fit(context,positions)

        print(str(len(objcluster)) + ' objects with the material ' + material)
        labels = db.labels_
        clusters = {}
        
        for cn, obj in zip(labels,objcluster):
            if cn not in clusters:
                clusters[cn] = [obj]
            else:
                clusters[cn].append(obj)

        processed_clusters[material] = clusters
        
        for x,y in clusters.items():
            print("Cluster " + str(x) + " has " + str(len(y)) + " items")

    for material, objcluster in processed_clusters.items():
        for cn, clusters in objcluster.items():
            bpy.ops.object.select_all(action='DESELECT')
            for obj in clusters:
                obj.select_set(state=True)
            
            bpy.context.view_layer.objects.active = clusters[0]
            print("Merging " + str(len(clusters)) + " items.")
            bpy.ops.object.join()

def SplitByMaterial(objects):
    unique_colors = {}

    print("Total object count: " + str(len(objects)))
    # Sort all objects by their material. Ignore objects with more than one material for now.
    for obj in objects:
        if len(obj.material_slots) > 1:
            print(str(len(obj.material_slots)) + ' materials in '+ obj.name + '. Ignoring.')
            continue
        for mat in obj.material_slots:
            if mat.name not in unique_colors:
                unique_colors[mat.name] = [obj]
            else:
                unique_colors[mat.name].append(obj)

    print("\nFound " + str(len(unique_colors)) + " different materials. \n")

    return unique_colors

class ClusterGroupProperty(bpy.types.PropertyGroup):
    mode_options = [(value, value, '', idx) for idx, value in enumerate(clustering_algorithm)]
    
    Mode: bpy.props.EnumProperty(
        items=mode_options,
        name="Clustering mode",
        description="Clustering mode",
        default='DBSCAN'
    )

    SelectedOnly: bpy.props.BoolProperty(name="Only process selected objects")
    ByMaterial: bpy.props.BoolProperty(name="Split clusters by material")
    MinSamples: bpy.props.IntProperty(name="Min samples",default=3)

    Eps: bpy.props.FloatProperty(name="EPS",default=0.5)

    Xi: bpy.props.FloatProperty(name="XI",default=0.05)
    MinClusterSize: bpy.props.FloatProperty(name="Min cluster size",default=0.05)


class OBJECT_OT_ClusteringCore(bpy.types.Operator):
    """Object clustering"""
    bl_idname = "object.cluster"
    bl_label = "Cluster and merge"
    bl_options = {'REGISTER','UNDO','INTERNAL'}
    
    def execute(self,context):
        ProcessClustering(self, context)
        return {'FINISHED'}

class CLUSTERING_PT_ClusteringPanel(bpy.types.Panel):
    """Panel for clustering params"""
    bl_label = 'Clustering'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self,context):
        layout = self.layout
        col = layout.column()

        col.prop(context.scene.clustering_group, "Mode")
        col.prop(context.scene.clustering_group, "SelectedOnly")
        col.prop(context.scene.clustering_group, "ByMaterial")
        col.prop(context.scene.clustering_group, "MinSamples")

        if context.scene.clustering_group.Mode == 'DBSCAN':
            col.prop(context.scene.clustering_group, "Eps")
        elif context.scene.clustering_group.Mode == 'OPTICS':
            col.prop(context.scene.clustering_group, "Xi")
            col.prop(context.scene.clustering_group, "MinClusterSize")
        else:
            pass

        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.cluster")
 
 
classes = (
    ClusterGroupProperty,
    OBJECT_OT_ClusteringCore,
    CLUSTERING_PT_ClusteringPanel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.clustering_group = bpy.props.PointerProperty(type=ClusterGroupProperty)

def unregister():
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.clustering_group

if __name__ == "__main__":
    register()
