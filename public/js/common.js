function ApiHelper(data) {
    const url = data.method=='get' && data.data != undefined?data.url+data.data:data.url
    return fetch(url, {
      // Return promise
      method: data.method,
      withCredentials: true,
      // credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data.method != 'get'?JSON.stringify(data.data):null,
    })
      .then((res) => res.json())
      .then(
        (result) => {
          return result;
        },
        (error) => {
          return error;
        }
      );
  }