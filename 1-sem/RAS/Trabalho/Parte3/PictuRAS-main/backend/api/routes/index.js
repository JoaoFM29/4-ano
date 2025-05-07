var express = require('express');
var router = express.Router();
var passport = require('passport');
var axios = require('axios');
var userModel = require('../models/user');
var User = require('../controllers/user');
const multer = require('multer');
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
const FormData = require('form-data');

router.get('/', function (req, res) {
  res.jsonp('Im here. My name is api')
})

// done
router.post('/register', async function (req, res) {
  try {
    // Check if user exists first
    const existingUser = await User.checkUserExistence(req.body.username);
    if (existingUser) {
      return res.status(400).jsonp({ error: 'User already exists' });
    }

    // Get the free plan ID
    let freePlanId = null;
    const plansMicroservice = process.env.PLANS_MICRO_SERVICE;
    
    try {
      const response = await axios.get(`${plansMicroservice}/plans`);
      const freePlan = response.data.find(plan => plan.name.toLowerCase() === 'free');
      if (freePlan) {
        freePlanId = freePlan.id;
      } else {
        console.warn('Free plan not found');
      }
    } catch (error) {
      console.error('Error fetching plans:', error.message);
      // Continue with null freePlanId rather than failing the registration
    }

    // Create the date string
    const d = new Date().toISOString().substring(0, 19);

    // Register the user
    const user = await new Promise((resolve, reject) => {
      userModel.register(
        new userModel({
          username: req.body.username,
          dateCreated: d,
          dateAccessed: d
        }), 
        req.body.password,
        (err, user) => {
          if (err) reject(err);
          else resolve(user);
        }
      );
    });

    // Create user in microservice
    const newUser = {
      username: req.body.username,
      password_hash: user.hash,
      name: req.body.name,
      email: req.body.email,
      type: "registered",
      plan: freePlanId,
    };

    const apiBaseUrl = process.env.USERS_MICRO_SERVICE;
    await axios.post(`${apiBaseUrl}/users`, newUser);
    
    res.jsonp('User registered with success!');

  } catch (error) {
    console.error('Registration error:', error);
    const statusCode = error.response?.status || 500;
    const errorMessage = error.response?.data || error.message;
    res.status(statusCode).jsonp({ 
      error: "Registration failed", 
      details: errorMessage 
    });
  }
});

// done
router.post('/login', (req, res, next) => {
  passport.authenticate('local', async (err, user, info) => {
    if (err) {
      console.error('Authentication error:', err);
      return res.status(500).json({ message: 'Internal server error' });
    }

    if (!user) {
      // If authentication failed, return the error message provided by Passport
      return res.status(401).json({ message: info?.message || 'Invalid credentials' });
    }

    // Log the user in and update their dateAccessed
    req.logIn(user, async (loginErr) => {
      if (loginErr) {
        console.error('Login error:', loginErr);
        return res.status(500).json({ error: "Failed to log in server error", message: 'Failed to log in' });
      }

      try {
        const date = new Date().toISOString().substring(0, 19); // Current timestamp
        await User.updateUser(user.username, { dateAccessed: date }); // Update user's last accessed date
        res.status(200).json({ message: 'Login successful', sessionId: req.sessionID });
      } catch (updateErr) {
        console.error('Error updating user access date:', updateErr);
        res.status(500).json({ message: 'Error updating user access date' });
      }
    });
  })(req, res, next);
});

// done
router.post('/logout', function (req, res) {
  req.logout(function (err) {
    if (err) return res.status(500).json({ error: err });
    res.json({ message: "Logged out successfully" });
  });
});

// done
router.get('/profile', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  try{
  if (req.isAuthenticated()) {
    // request ao micro serviço a info do user
    const apiBaseUrl = process.env.USERS_MICRO_SERVICE // Ensure this is set in your .env file
    // Make the GET request to the external API
    const response = await axios.get(`${apiBaseUrl}/users/${req.user.username}`);
    res.status(200).jsonp({ email: response.data.email, name: response.data.name, plan: response.data.plan });
  } else {
    res.status(401).jsonp({ error: "Not authenticated" });
  }
  }catch(e){
    console.error(e);
  }
});

// done
router.get('/user/status', passport.authenticate(['local', 'anonymous'], { session: false }), (req, res) => {
  if (req.isAuthenticated()) {
    res.json({ status: 'loggedIn', sessionId: req.sessionID });
  } else {
    res.json({ status: 'anonymous', sessionId: req.sessionID });
  }
});

//done
router.get('/tools', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  try {
    // Use the API base URL from your environment variables
    const apiBaseUrl = process.env.TOOL_MICRO_SERVICE // Ensure this is set in your .env file
    // Make the GET request to the external API
    console.log(`${apiBaseUrl}/tools`)
    const response = await axios.get(`${apiBaseUrl}/tools`);
    // Optionally process the response.data here if needed
    const staticTools = response.data;
    return res.status(200).json(staticTools)

  } catch (error) {
    // Handle errors and send an appropriate response
    console.error('Error fetching tools:', error.message);

    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch tools',
      details: error.response?.data || error.message,
    });
  }
});

// done
router.get('/projects', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  try {
    // logica de enviar const = axios.get wtv
    // localhost:3003/projects/owner/<user_id></user_id>
    if (req.isAuthenticated()) {

      const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
      const response = await axios.get(`${apiBaseUrl}/projects/owner/${req.user.username}`);
      return res.status(200).json(response.data);

    } else {
      const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
      const response = await axios.get(`${apiBaseUrl}/projects/owner/anonymous-${req.sessionID}`);
      return res.status(200).json(response.data);
    }

  } catch (error) {
    // Handle errors and send an appropriate response
    console.error('Error fetching projects:', error.message);

    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch projects',
      details: error.response?.data || error.message,
    });
  }
});

// done (testar para registados)
router.post('/projects', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  if (req.isAuthenticated()) {
    try{
    const { name, owner } = req.body;
    // Create a new project
    const newProjectWrapper = {
      name: name || 'Untitled', // Default to 'Untitled' if no name is provided
      owner: req.user.username, // Use user ID if authenticated, otherwise use session ID
      tools: []
    };
    const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
    const response = await axios.post(`${apiBaseUrl}/projects`, newProjectWrapper);
    const newProject = response.data;
    res.json(newProject);
  } catch(e){
    console.error(e)
  }
  } else {
    try {
      const { name, owner } = req.body;
      // Create a new project
      const newProjectWrapper = {
        name: name || 'Untitled', // Default to 'Untitled' if no name is provided
        owner: `anonymous-${req.sessionID}`, // Use user ID if authenticated, otherwise use session ID
        tools: []
      };
      const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
      const response = await axios.post(`${apiBaseUrl}/projects`, newProjectWrapper);
      const newProject = response.data;
      res.json(newProject);
    } catch (e) {
      console.error(e)
    }
  }
});

// todo testar isto
router.post(
  '/projects/images',
  upload.single('image'),
  passport.authenticate(['local', 'anonymous'], { session: false }),
  async (req, res) => {
    const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
    if (req.isAuthenticated()) {
      try {
        // Handle the anonymous user case
        // Extract `projectId` and process the image file

        const projectId = req.body.projectId;
        if (!projectId) {
          return res.status(400).json({ error: 'Project ID is required.' });
        }

        // Assume `req.file` has the uploaded image (if using middleware like multer)
        const file = req.file;
        if (!file) {
          return res.status(400).json({ error: 'No image provided.' });
        }
        const formData = new FormData();
        formData.append("image", file.buffer, file.originalname);
        const response = await axios.post(`${apiBaseUrl}/projects/images/${projectId}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          }
        });
        return res.status(200).json(response.data);
      } catch (e) {
        console.error('Error uploading file for anonymous user:', e);
        return res.status(500).json({ error: 'Internal server error.' });
      }
    } else {
      try {
        // Handle the anonymous user case
        // Extract `projectId` and process the image file

        const projectId = req.body.projectId;
        if (!projectId) {
          return res.status(400).json({ error: 'Project ID is required.' });
        }

        // Assume `req.file` has the uploaded image (if using middleware like multer)
        const file = req.file;
        if (!file) {
          return res.status(400).json({ error: 'No image provided.' });
        }
        const formData = new FormData();
        formData.append("image", file.buffer, file.originalname);
        const response = await axios.post(`${apiBaseUrl}/projects/images/${projectId}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          }
        });
        return res.status(200).json(response.data);
      } catch (e) {
        console.error('Error uploading file for anonymous user:', e);
        return res.status(500).json({ error: 'Internal server error.' });
      }
    }
  }
);

// todo - `GET localhost:3003/projects/images/<project_id>`: obter as imagens do projeto 
router.get('/projects/images', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE

  try {
    const { projectId } = req.query;
    const uris = await axios.get(`${apiBaseUrl}/projects/images/${projectId}`);
    res.status(200).json(uris.data)

  } catch (e) {
    console.error(e)
  }

});

// pedir bytes de image uma a uma
router.get('/projects/images/:id', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
  axios.get(`${apiBaseUrl}/projects/images/data/${req.params.id}`, { responseType: 'arraybuffer' })
    .then(response => {
      res.contentType(response.headers.get('content-type'))
      res.status(200).send(response.data)
    })
    .catch(error => res.status(500).jsonp(error))
});

// done (testar para autenticado)
router.put('/projects', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  if (req.isAuthenticated()) {
    try{
    const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
    const response = await axios.put(`${apiBaseUrl}/projects/${req.body.id}`, req.body)
    res.status(200).json(`Sucess on saving ${req.body.id}`);
    } catch(e){
      console.error(e)
    }
  } else {
    try {
      const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE
      const response = await axios.put(`${apiBaseUrl}/projects/${req.body.id}`, req.body)
      res.status(200).json(`Sucess on saving ${req.body.id}`);
    } catch (e) {
      console.error(e)
    }
  }
});

router.delete('/projects/images', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE

      try{
        const { images } = req.query;
        for(id in images){
          await axios.delete(`${apiBaseUrl}/projects/images/${images[id]}`);
        }
        res.status(200).json(`Success on deleting the images!`);

      }catch(e){
        console.error(e)
        res.status(500).json(`Server error`);
      }
      
});


router.delete('/projects/:id', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  const projectId = req.params.id; // Obter o ID do projeto da URL
  const apiBaseUrl = process.env.PROJECTS_MICRO_SERVICE; // URL do microserviço

  try {
    if (req.isAuthenticated()) {
      const response = await axios.delete(`${apiBaseUrl}/projects/${projectId}`, {
        withCredentials: true,
      });

      res.status(response.status).json({
        message: 'Project deleted successfully',
        data: response.data,
      });
    } else {
      res.status(401).json({
        error: 'Unauthorized',
        details: 'User must be authenticated to delete a project.',
      });
    }
  } catch (error) {
    console.error('Error deleting project:', error.message);

    res.status(error.response?.status || 500).json({
      error: 'Failed to delete project',
      details: error.response?.data || error.message,
    });
  }
});

router.put(
  '/user/plan',
  passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
    console.log('aaaaaaaaaaaa');
    if (!req.isAuthenticated()) {
      return res.status(401).json({
        error: 'Unauthorized',
        details: 'User must be authenticated to change the plan.',
      });
    }

    console.log('Authenticated user:', req.user);
    console.log('Incoming request body:', req.body);
    const { plan } = req.body;
    if (!plan) {
      return res.status(400).json({ error: 'Bad Request', details: 'Plan is required.' });
    }

    const apiBaseUrl = process.env.USERS_MICRO_SERVICE;

    try {
      const response = await axios.put(
        `${apiBaseUrl}/users/${req.user.username}`,
        { plan }
      );
      res.status(200).json({
        message: 'Plan updated successfully',
        data: response.data,
      });
    } catch (error) {
      console.error('Error updating user plan:', error.message);
      res.status(error.response?.status || 500).json({
        error: 'Failed to update user plan',
        details: error.response?.data || error.message,
      });
    }
  }
);

router.get('/plans', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {

  const apiBaseUrl = process.env.PLANS_MICRO_SERVICE;
  try {
    const response = await axios.get(`${apiBaseUrl}/plans`);
    res.status(200).json(response.data);
  } catch (error) {
    console.error('Error fetching plans:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to fetch plans',
      details: error.response?.data || error.message,
    });
  }
});


router.get('/plan/:planId', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  if (req.isAuthenticated()) {
    const apiBaseUrl = process.env.PLANS_MICRO_SERVICE;
    try {
      const response = await axios.get(`${apiBaseUrl}/plans/${req.params.planId}`);
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching plans:', error.message);
      res.status(error.response?.status || 500).json({
        error: 'Failed to fetch plans',
        details: error.response?.data || error.message,
      });
    }
  }
  else {
    res.status(401).json({ error: 'Unauthorized', details: 'User must be authenticated to access plan details.' });
  }
});

router.get('/users/:email', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  console.log('GET EMAIL');
  const email = req.params.email; // Email passado como parâmetro na URL
  console.log('GET EMAIL:', email);

  const apiBaseUrl = process.env.USERS_MICRO_SERVICE;

  try {
      console.log('Fetching user data from:', `${apiBaseUrl}/users/${email}`);
      const response = await axios.get(`${apiBaseUrl}/users/${email}`);

      // Enviar resposta com os dados do usuário
      res.status(200).json({
          message: 'User data fetched successfully',
          data: response.data,
      });
  } catch (error) {
      console.error('Error fetching user data:', error.message);
      res.status(error.response?.status || 500).json({
          error: 'Failed to fetch user data',
          details: error.response?.data || error.message,
      });
  }
});

router.delete('/users/:email', passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
  const email = req.params.email; // Email passado como parâmetro na URL
  const apiBaseUrl = process.env.USERS_MICRO_SERVICE;

  try {
    console.log(`Attempting to delete user with email: ${email}`);

    // Enviar a requisição DELETE ao microserviço de usuários
    const response = await axios.delete(`${apiBaseUrl}/users/${email}`, {
      withCredentials: true, // Certifique-se de que está enviando cookies/certificados necessários
    });

    // Enviar resposta de sucesso
    res.status(response.status).json({
      message: 'User deleted successfully',
      data: response.data,
    });

  } catch (error) {
    console.error('Error deleting user:', error.message);
    res.status(error.response?.status || 500).json({
      error: 'Failed to delete user',
      details: error.response?.data || error.message,
    });
  }
});

router.put(
  '/users/:email',
  passport.authenticate(['local', 'anonymous'], { session: false }), async (req, res) => {
    console.log('PUT EMAIL');
    const email = req.params.email; // Email passado como parâmetro na URL
    console.log('PUT EMAIL:', email);
    
    const apiBaseUrl = process.env.USERS_MICRO_SERVICE;

    // O corpo da requisição será ignorado e o nome será sempre "qqq5"
    // const newProfile = { name: "qqq5" };
    const newProfile = { name: req.body.name }; // Só o campo 'name' será enviado

    console.log('Sending PUT request to:', `${apiBaseUrl}/users/${email}`);
    console.log('New profile being sent:', newProfile);

    try {    
      console.log('AQUI'); 
      console.log('RESPONSE:', `${apiBaseUrl}/users/${email}`); 
      const response = await axios.put(
        `${apiBaseUrl}/users/${email}`,
        newProfile 
      );

      // Enviar resposta de sucesso
      res.status(200).json({
        message: 'newProfile updated successfully',
        data: response.data,
      });
    } catch (error) {
      console.error('Error updating user newProfile:', error.message);
      res.status(error.response?.status || 500).json({
        error: 'Failed to update user newProfile',
        details: error.response?.data || error.message,
      });
    }
  }
);

module.exports = router;
