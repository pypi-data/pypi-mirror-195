import pytest

from firepit.query import Column, Filter, Predicate, Query, Table
from firepit.sqlstorage import get_path_joins


# Test utility data and functions
def _make_query(etype: str, attr: str, value: int):
    '''Simulate ECGPComparison'''
    joins, target_table, target_column = get_path_joins(None, etype, attr)
    if target_table:
        col = Column(target_column, table=target_table)
    else:
        col = attr
    qry = Query([Table(etype), Filter([Predicate(col, "=", value)])])
    if joins:
        # Need to explicitly self the lhs of the join?
        for j in joins:
            j.prev_name = etype
        qry.joins = joins
    return qry


#TODO: move this somewhere
def _merge_queries(lhs: Query, op: str, rhs: Query):
    result = Query(lhs.table)
    result.joins = lhs.joins + rhs.joins
    assert len(lhs.where) == 1
    assert len(lhs.where[0].preds) == 1
    assert len(rhs.where) == 1
    assert len(rhs.where[0].preds) == 1
    lpred = lhs.where[0].preds[0]
    rpred = rhs.where[0].preds[0]
    result.where.append(Filter([Predicate(lpred, op, rpred)]))
    return result


@pytest.mark.parametrize(
    "op",
    [
        "AND",
        "OR",
    ],
)
def test_merge_op(op):
    q1 = _make_query("foo", "attr1", 1)
    q2 = _make_query("foo", "attr2", 2)
    q3 = _merge_queries(q1, op, q2)
    qtext, values = q3.render("?")
    assert qtext == f'SELECT * FROM "foo" WHERE (("attr1" = ?) {op} ("attr2" = ?))'
    assert values == (1, 2)

    q4 = _make_query("foo", "attr3", 3)
    q5 = _merge_queries(q3, op, q4)
    qtext, values = q5.render("?")
    # FIXME: this one generates extra parens around first 2 comps
    assert qtext == (
        'SELECT * FROM "foo" WHERE'
        # f' (("attr1" = ?) {op} ("attr2" = ?) {op} ("attr3" = ?))')
        f' ((("attr1" = ?) {op} ("attr2" = ?)) {op} ("attr3" = ?))'
    )
    assert values == (1, 2, 3)


def test_merge_joins():
    etype = "network-traffic"
    attr1 = "src_ref.value"
    q1 = _make_query(etype, attr1, "10.0.0.1")
    # print(q1.render('XXX'))
    pred = q1.where[0].preds[0]
    print(q1.table.name, q1.joins, pred.lhs, pred.op, pred.rhs)
    attr2 = "dst_ref.value"
    q2 = _make_query(etype, attr2, "9.9.9.9")
    pred = q2.where[0].preds[0]
    print(q2.table.name, q2.joins, pred.lhs, pred.op, pred.rhs)

    q3 = _merge_queries(q1, "AND", q2)
    pred = q3.where[0].preds[0]
    print(q3.table.name, q3.joins, pred.lhs.render("A"), pred.op, pred.rhs.render("B"))
    qtext, values = q3.render("?")
    assert qtext == (
        'SELECT * FROM "network-traffic"'
        ' INNER JOIN "ipv4-addr" AS "src" ON "network-traffic"."src_ref" = "src"."id"'
        ' INNER JOIN "ipv4-addr" AS "dst" ON "network-traffic"."dst_ref" = "dst"."id"'
        ' WHERE (("src"."value" = ?) AND ("dst"."value" = ?))'
    )
    assert values == ("10.0.0.1", "9.9.9.9")
