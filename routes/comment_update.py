from database import database


def update(tp_status, id_comment_internal):
    conn = database.connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE 
            comment 
        SET 
            tp_status = %s 
        WHERE 
            id_comment_internal = %s
    """, (
        tp_status,
        id_comment_internal
    ))
    rows_updated = cursor.rowcount

    if rows_updated == 0:
        return False

    conn.commit()
    cursor.close()
    conn.close()

    return True
