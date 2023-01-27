from localocpa.objects.log.ocel import OCEL
from localocpa.objects.log.variants.table import Table
from localocpa.objects.log.variants.graph import EventGraph
import localocpa.objects.log.importer.csv.versions.to_obj as obj_importer
import localocpa.objects.log.variants.util.table as table_utils
def remove_object_references(df, object_types, to_keep):
    for ot in object_types:
        df[ot] = df[ot].apply(lambda x: list(set(x) & to_keep[ot]))
    df = df[df[object_types].astype(bool).any(axis=1)]
    return df

def copy_log(ocel):
    df = ocel.log.log
    log = Table(df, parameters=ocel.parameters)
    obj = obj_importer.apply(df, parameters=ocel.parameters)
    graph = EventGraph(table_utils.eog_from_log(log))
    new_log = OCEL(log, obj, graph, ocel.parameters)
    return new_log

def copy_log_from_df(df, parameters):
    log = Table(df, parameters=parameters)
    obj = obj_importer.apply(df, parameters=parameters)
    graph = EventGraph(table_utils.eog_from_log(log))
    new_log = OCEL(log, obj, graph, parameters)
    return new_log

def get_objects_of_variants(ocel, variants):
    obs = {}
    for ot in ocel.object_types:
        obs[ot] = set()
    for v_id in variants:
        for case_id in ocel.variants_dict[ocel.variants[v_id]]:
            for ob in ocel.process_execution_objects[case_id]:
                obs[ob[0]].add(ob[1])

    return obs
