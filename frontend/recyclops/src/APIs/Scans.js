export const getScans = async (id) => {
  return fetch(`${import.meta.env.VITE_NODE_JS_PORT}/scan/getData/${id}`).then(
    async (data) => {
      return await data.json();
    }
  );
};

export const getRecentScansId = async (user) => {
  return fetch(
    `${import.meta.env.VITE_NODE_JS_PORT}/user/scanHistory/${user.uid}`
  ).then(async (data) => await data.json());
};

export const getSavedScansId = async (user) => {
  return fetch(
    `${import.meta.env.VITE_NODE_JS_PORT}/user/savedScan/${user.uid}`
  ).then(async (data) => await data.json());
};

export const scanImage = async (uri, userId = null) => {
  const body = {
    userId: userId,
    dataURI: uri,
  };
  return fetch(`${import.meta.env.VITE_NODE_JS_PORT}/scan/newScan/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  }).then(async (data) => await data.json());
};
