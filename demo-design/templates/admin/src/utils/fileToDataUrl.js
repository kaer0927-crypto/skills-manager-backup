/**
 * 把 File 转为 dataURL，附带大小 / 类型校验。
 * @param {File} file
 * @param {Object} [opts]
 * @param {number} [opts.maxSizeMB=5]
 * @param {string[]} [opts.accept=['image/jpeg', 'image/png']]
 * @returns {Promise<string>} dataURL
 */
export function fileToDataUrl(
  file,
  { maxSizeMB = 5, accept = ['image/jpeg', 'image/png'] } = {}
) {
  return new Promise((resolve, reject) => {
    if (!accept.includes(file.type)) {
      const exts = accept.map((t) => t.replace('image/', '')).join(' / ')
      return reject(new Error(`仅支持 ${exts} 格式`))
    }
    if (file.size > maxSizeMB * 1024 * 1024) {
      return reject(new Error(`文件不能超过 ${maxSizeMB}MB`))
    }
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(new Error('文件读取失败'))
    reader.readAsDataURL(file)
  })
}
