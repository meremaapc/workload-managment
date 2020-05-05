import domain.query_constant
from util.workload_service import calculate_process_workload, get_metrics, get_info_about_all_pg_processes, \
    metrics_to_dict


def select_resource_intensive_process(processes, host_connection, wm_db_connection):
    metrics = get_metrics(wm_db_connection)
    # todo ?maybe need kill recent process
    processes_info = get_info_about_all_pg_processes(host_connection, processes,
                                                     list(map(lambda metric: metric['name'], metrics)))
    metrics = metrics_to_dict(metrics)
    result = max(zip(
        map(lambda process: calculate_process_workload(process, metrics), processes_info),
        map(lambda process: process['pid'], processes_info))
    )
    return result[1]


def kill_process_by_pid(pid, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(domain.query_constant.PG_CANCEL_BACKEND % pid)
        print("Killed pid", pid, sep=" ")
    except Exception as error:
        print(error)
    finally:
        if conn and cursor:
            cursor.close()
