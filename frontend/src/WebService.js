import axios from 'axios';

// const url  = 'https://jsonplaceholder.typicode.com/'
const url  = 'http://127.0.0.1:8000/api/'

class WebService {
  // GET REQUEST
  static get(uri) {
    return new Promise(async (resolve, reject) => {
      try {
        const res = await axios.get(url+uri)
        const data = res.data
        resolve(data)
      } catch(err) {
        reject(err)
      }
    })
  }

  // POST REQUEST
  static post(uri, obj) {
    return axios.post(url+uri, {
      obj
    })
  }

  // DELETE REQUEST
  static del(uri) {
    return axios.delete(url+uri)
  }
  
  // PUT REQUEST
  static put(uri, obj) {
    return axios.put(url+uri, {
      obj
    })
  }
}

export default WebService;
