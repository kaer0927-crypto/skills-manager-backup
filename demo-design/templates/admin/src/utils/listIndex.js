/**
 * 把行索引 + 当前分页信息换算成跨页连续的显示序号：`(page-1)*pageSize + i + 1`。
 * @param {number} page 当前页码（1-based）
 * @param {number} pageSize 每页大小
 * @returns {(i: number) => number} 序号函数
 */
export function makeIndex(page, pageSize) {
  const base = (page - 1) * pageSize
  return (i) => base + i + 1
}
