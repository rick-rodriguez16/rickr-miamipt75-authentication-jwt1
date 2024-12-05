const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			token: null
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			
			// handle the process requesting a token
			// if successful, it will put the token string
			// in the store to allow for future use
			login: async (email, password) => {
				const options = {
					method: 'POST',
					mode: 'cors',
					headers : {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						email: email,
						password: password
					})
				}

				const response = await fetch('http://localhost:3001/api/token', options)

				if (!response.ok) {
					console.log("Error: ", response.statusText, response.status)
					return false;
				}

				const data = await response.json();
				console.log('This came from the backend: ', data);
				setStore({token: data.access_token})
				return true;
			}


			// signup action
			// validation action
			// logout action
		}
	};
};

export default getState;
