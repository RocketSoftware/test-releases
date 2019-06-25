const https = require('https')


createRelease = function(version) {
  auth = "Basic " + new Buffer.from('hrensink' + ":" + 'R0cket1!').toString("base64");
  
  const options = {
    host: 'api.github.com',
    port: '443',
    path: '/repos/RocketSoftware/test-releases/releases',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent' : 'hrensink@rocketsoftware.com',
      'Authorization' : auth
    }
  }

  const req = https.request(options, (res) => {
    console.log(`statusCode: ${res.statusCode}`)

    res.on('data', (d) => {
//      process.stdout.write(d)
    })

    res.on('end', function() {
      // console.log("Finished")
    });
  })
  
  req.on('error', (error) => {
    console.error(error)
  })

  const payload = {
    tag_name : version,
    target_commitish: 'master',
    name : version,
    body : 'Bamboo build',
    draft : false,
    prerelease: true
  }  

  req.write(JSON.stringify(payload))
  req.end()
}

getReleases = function() {
  const options = {
    host: 'api.github.com',
    port: '443',
    path: '/repos/RocketSoftware/test-releases/releases',
    method: 'GET',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent' : 'hrensink@rocketsoftware.com'
    }
  }

  const req = https.request(options, (res) => {
    var msg = '';
  
    res.on('data', (d) => {
      msg += d;
    })
    
    res.on('end', function() {
      payload = JSON.parse(msg);
      console.log(payload.length + " releases")
      // console.log(payload);
    });
  })
  
  req.on('error', (error) => {
    console.error(error)
  })
  
  req.end()
}

createRelease('v1.0.6')
