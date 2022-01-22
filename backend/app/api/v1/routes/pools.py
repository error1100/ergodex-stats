#region imports
from optparse import Option
from fastapi import APIRouter, Request, Query, Path
from typing import Optional
#endregion

#region main
pools_router = r = APIRouter()

@r.get(
    "/"
)
async def get_pools(request: Request):
    """
    Get available pools
    """
    query = """
        SELECT 
            DISTINCT pool_id
            ,CONCAT(COALESCE(x.ticker,'Unknown'),'-',COALESCE(y.ticker,'Unknown')) AS pool_name
        FROM pools p
        LEFT JOIN assets x ON p.x_id = x.id
        LEFT JOIN assets y ON p.y_id = y.id
    """
    async with request.app.state.db.acquire() as conn:
        res = await conn.fetch(query)
    return res

@r.get(
     "/{pool_id}/{min_gix}"
)
async def get_pool_snapshot_mingix(
        request: Request,
        pool_id: str = Path(..., title='Id of LP pool.'),
        min_gix: int = Path(..., title='Minimum global index.'),
        offset: Optional[int] = Query(0,ge=0),
        limit: Optional[int] = Query(100,ge=1,le=1000)
    ):
    """
    Get stats for pool
    """
    query = f"""
        SELECT
            a_x.ticker as x_ticker, x_amount/POWER(10,a_x.decimals) as x_amount, 
            a_y.ticker as y_ticker, y_amount/POWER(10,a_y.decimals) as y_amount, 
            x_amount/POWER(10,a_x.decimals)*y_amount/POWER(10,a_y.decimals) as k,
            y_amount/POWER(10,a_y.decimals)/x_amount/POWER(10,a_x.decimals) as p,
            gindex
        FROM pools p
        LEFT JOIN assets a_x ON a_x.id = p.x_id
        LEFT JOIN assets a_y ON a_y.id = p.y_id
        WHERE pool_id = '{pool_id}' AND gindex >= {min_gix}
        ORDER BY gindex ASC
        LIMIT {limit} 
        OFFSET {offset} 
    """
    async with request.app.state.db.acquire() as conn:
        res = await conn.fetch(query)
    return res

#endregion