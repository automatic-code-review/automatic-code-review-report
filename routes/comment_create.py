from database import database


def create(json_data):
    conn = database.connection()
    cursor = conn.cursor()

    merge_data = json_data['merge']
    cursor.execute("""
        SELECT 
            id_merge_internal
        FROM 
            merge
        WHERE
            id_merge = %s AND
            id_project = %s AND
            id_group = %s
    """, (
        merge_data['idMerge'],
        merge_data['idProject'],
        merge_data['idGroup']
    ))
    merge_id = cursor.fetchone()

    if merge_id:
        merge_id = merge_id[0]
    else:
        cursor.execute("""
            INSERT INTO merge (
                id_merge,
                id_project,
                id_group,
                ds_author_username,
                dh_merge
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            ) RETURNING id_merge_internal
        """, (
            merge_data['idMerge'],
            merge_data['idProject'],
            merge_data['idGroup'],
            merge_data['dsAuthorUsername'],
            merge_data['dhMerge']
        ))
        merge_id = cursor.fetchone()[0]

    comments_data = json_data['comments']
    for comment_data in comments_data:
        cursor.execute("""
            SELECT 
                id_comment_internal
            FROM 
                comment
            WHERE
                id_comment = %s AND
                id_merge_internal = %s
        """, (
            comment_data['idComment'],
            merge_id
        ))
        comment_id = cursor.fetchone()

        if not comment_id:
            cursor.execute("""
                INSERT INTO comment (
                    id_merge_internal, 
                    id_comment, 
                    lk_comment, 
                    ds_type, 
                    tx_comment
                ) VALUES (
                    %s, 
                    %s, 
                    %s, 
                    %s, 
                    %s
                )
            """, (
                merge_id,
                comment_data['idComment'],
                comment_data['lkComment'],
                comment_data['dsType'],
                comment_data['txComment']
            ))

    conn.commit()
    cursor.close()
    conn.close()
