from database import database


def read_workspaces(tp_status):
    conn = database.connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            M.ds_workspace_name,
            COUNT( * ) AS qt_pendente
        FROM 
            comment C JOIN merge M on C.id_merge_internal = M.id_merge_internal
        WHERE
            C.tp_status = 0
        GROUP BY
            M.ds_workspace_name
        """, ()
    )
    rows = cursor.fetchall()

    workspaces = []
    for row in rows:
        workspace = {
            'dsName': row[0],
            'qtPendente': row[1]
        }
        workspaces.append(workspace)

    return workspaces


def read(tp_status, page_size, page_number, workspace_name):
    conn = database.connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COUNT( * ) 
        FROM 
            comment C JOIN merge M on C.id_merge_internal = M.id_merge_internal
        WHERE
            C.tp_status = %s AND
            M.ds_workspace_name = %s
    """, (
        tp_status,
        workspace_name
    ))
    total_count = cursor.fetchone()[0]

    page_total = (total_count + page_size - 1) // page_size
    offset = (page_number - 1) * page_size

    cursor.execute("""
        SELECT
            C.id_comment_internal,
            C.lk_comment,
            C.ds_type,
            C.tx_comment,
            M.ds_author_username,
            C.tp_status,
            M.ds_workspace_name
        FROM
            comment C JOIN merge M on C.id_merge_internal = M.id_merge_internal
        WHERE
            C.tp_status = %s AND
            M.ds_workspace_name = %s
        ORDER BY
            C.id_comment_internal
        LIMIT
            %s
        OFFSET
            %s
    """, (tp_status, workspace_name, page_size, offset))
    rows = cursor.fetchall()

    comentarios = []
    for row in rows:
        comment = {
            'idCommentInternal': row[0],
            'lkComment': row[1],
            'dsType': row[2],
            'txComment': row[3],
            'dsAuthorUsername': row[4],
            'tpStatus': row[5],
            'dsWorkspaceName': row[6],
        }
        comentarios.append(comment)

    has_next = page_number < page_total

    cursor.close()
    conn.close()

    return {
        'data': comentarios,
        'qtPage': page_total,
        'qtTotal': total_count,
        'nrPageNumber': page_number,
        'nrPageSize': page_size,
        'hasNext': has_next
    }
