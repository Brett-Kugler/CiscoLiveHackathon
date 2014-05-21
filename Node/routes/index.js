process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
var express = require('express');
var router = express.Router();
var request = require('request');
var parseString = require('xml2js').parseString;
var twiliokeys = require('../secretkeys.js');
var twilioclient = require('twilio')(twiliokeys.TWILIO_ACCOUNT_SID, twiliokeys.TWILIO_AUTH_TOKEN);

// Type 3: Persistent datastore with automatic loading
var Datastore = require('nedb')
  , db = new Datastore({ filename: './database', autoload: true });
// You can issue commands right away

/* GET home page. */
//router.get('/', function(req, res) {
//    res.render('index', { title: 'Express' });
//});

//router.get('/test', function (req, res) {
//    res.end('{"success":"true"}');
//});

//router.get('/insertTestEvent', function (req, res) {
//    db.insert(req.query, function (err, newDocs) {
//        console.log(newDocs);
//        // Two documents were inserted in the database
//        // newDocs is an array with these documents, augmented with their _id
//    });

//    res.end('{"success":"true"}');
//});

router.get('/dropDB', function (req, res) {

    //// Remove multiple documents
    //db.remove({ system: 'solar' }, { multi: true }, function (err, numRemoved) {
    //    // numRemoved = 3
    //    // All planets from the solar system were removed
    //});

    // Remove multiple documents
    db.remove({}, { multi: true }, function (err, numRemoved) {
        // numRemoved = 3
        // All planets from the solar system were removed
        res.end('{"removed":' + numRemoved + '}');
    });

});

router.get('/countTempEvent', function (req, res) {

    //// Count all documents in the datastore
    //db.count({}, function (err, count) {
    //    // count equals to 4
    //});

    // Count all documents in the datastore
    db.count({}, function (err, count) {
        res.end('{"count":' + count + '}');
    });

});

router.get('/showDB', function (req, res) {

    //// Find all documents in the collection
    //db.find({}, function (err, docs) {
    //});

    // Find all documents in the collection
    db.find({}, function (err, docs) {
        res.json(docs);
    });

});

router.get('/testCMX', function (req, res) {
    //var macAddress = req.query.mac;
    
    //https://10.10.20.21/api/contextaware/v1/location/clients/

    request.get({
        uri: 'https://10.10.20.21/api/contextaware/v1/location/clients/',
        auth: {
            user: 'devuser',
            pass: 'devuser',
            sendImmediately: true
        }
        //headers: { Authorization: 'token ' + req.session.access_token }
    }, function (e, r, body) {
        try {
            console.log(body);
            res.end(body);
        } catch (e) {
            console.log("error: " + e);
            res.end('{"success":"false"}');
        }
    });
});

router.get('/testParseCMX', function (req, res) {
    //var macAddress = req.query.mac;

    //https://10.10.20.21/api/contextaware/v1/location/clients/

    request.get({
        uri: 'https://10.10.20.21/api/contextaware/v1/location/clients/',
        auth: {
            user: 'devuser',
            pass: 'devuser',
            sendImmediately: true
        }
        //headers: { Authorization: 'token ' + req.session.access_token }
    }, function (e, r, body) {
        try {

            //var xml = "<root>Hello xml2js!</root>"
            //parseString(xml, function (err, result) {
            //    console.dir(result);
            //});

            parseString(body, function (err, result) {
                console.log(result);

                res.json(result);
                //res.json(JSON.parse(result));
            });
        } catch (e) {
            console.log("error: " + e);
            res.end('{"success":"false"}');
        }
    });
});

//http://localhost:3000/findMAC?mac=3c:a9:f4:53:2d:cc
router.get('/findMAC', function (req, res) {
    var macAddress = req.query.mac;

    request.get({
        uri: 'https://10.10.20.21/api/contextaware/v1/location/clients/',
        auth: {
            user: 'devuser',
            pass: 'devuser',
            sendImmediately: true
        }
    }, function (e, r, body) {
        try {
            parseString(body, function (err, result) {
                var clients = [];

                function pushArrayElements(element, index, array) {
                    //console.log("client[" + index + "] = " + JSON.stringify(element)); //for debug
                    clients.push(element);
                    if(element.$.macAddress == macAddress) {
                        res.json(element);
                    }
                }
                result.Locations.WirelessClientLocation.forEach(pushArrayElements);

                if (result.Locations.WirelessClientLocation.count == clients.count) {
                    res.end('{"success":"false"}');
                }
            });
        } catch (e) {
            console.log("error: " + e);
            res.end('{"success":"false"}');
        }
    });
});

router.get('/findUserByMAC', function (req, res) {
    var macAddress = req.query.mac;

    db.find({'mac' : macAddress, 'type' : 'user'}, function (err, docs) {
        res.json(docs);
    });
});

//http://localhost:3000/findUserContacts?username=hc
router.get('/findUserContacts', function (req, res) {
    var username = req.query.username;

    db.find({ 'username': username, 'type': 'contact' }, function (err, docs) {
        res.json(docs);
    });
});

//http://localhost:3000/saveUser?username=hc&telephone=4156466297&mac=00:27:10:d3:51:78
router.get('/saveUser', function (req, res) {
    var username = req.query.username;
    var telephone = req.query.telephone;
    var mac = req.query.mac;

    db.insert({'username' : username, 'telephone' : telephone, 'mac' : mac, 'type' : 'user'}, function (err, newDocs) {
        console.log(newDocs);
        // Two documents were inserted in the database
        // newDocs is an array with these documents, augmented with their _id
        res.json(newDocs);
    });
});

//http://localhost:3000/saveUserContacts?username=hc&contactname=Harvey&telephone=4156466298&email=harvey@harveychan.net
router.get('/saveUserContacts', function (req, res) {
    var username = req.query.username;
    var contactname = req.query.contactname;
    var telephone = req.query.telephone;
    var email = req.query.email;

    db.insert({ 'username': username, 'contactname': contactname, 'telephone': telephone, 'email': email, 'type': 'contact' }, function (err, newDocs) {
        console.log(newDocs);
        // Two documents were inserted in the database
        // newDocs is an array with these documents, augmented with their _id
        res.json(newDocs);
    });
});

router.get('/quake', function (req, res) {
    var isQuake = req.query.quake;
    //var cmxUserInfo;
    if (!isQuake) {
        res.end('{"quake":' + isQuake + '}');
    }

    db.find({ 'type' : 'user' }, function (err, users) {
        var notifiedUsers = [];
        function pushArrayElements(element, index, array) {
            console.log("Notifying contacts for user: " + JSON.stringify(element)); //for debug
            //var cmxUserInfo;
            
            getCMXInfoByMac(element.mac, function (cmxUserInfo) {
                console.log('mac: ' + element.mac);
                console.log('cmx:' + cmxUserInfo);
                console.log('username:' + element.username);

                db.find({ 'username': element.username, 'type': 'contact' }, function (err, contacts) {
                    var smsNumbers = [];
                    function pushContactElements(element, index, array) {
                        //send sms here
                        //Send an SMS text message
                        sendSMS(cmxUserInfo, element);

                        smsNumbers.push(element);
                    }
                    users.forEach(pushContactElements);

                    if (smsNumbers.count == contacts.count) {
                        if (notifiedUsers.count == users.count) {
                            res.end('{"quake":' + isQuake + '}');
                        }
                    }
                });
            });
            
            //console.log(cmxUserInfo);

            notifiedUsers.push(element);
        }
        users.forEach(pushArrayElements);

        //if (notifiedUsers.count == users.count) {
        //    res.end('{"quake":' + isQuake + '}');
        //}
    });
});

function getCMXInfoByMac(mac, callback) {
    request.get({
        uri: 'https://10.10.20.21/api/contextaware/v1/location/clients/',
        auth: {
            user: 'devuser',
            pass: 'devuser',
            sendImmediately: true
        }
    }, function (e, r, body) {
        try {
            parseString(body, function (err, result) {
                var clients = [];

                function pushArrayElements(element, index, array) {
                    //console.log("client[" + index + "] = " + JSON.stringify(element)); //for debug
                    clients.push(element);
                    if (element.$.macAddress == mac) {
                        callback(element);
                    }
                }
                result.Locations.WirelessClientLocation.forEach(pushArrayElements);

                if (result.Locations.WirelessClientLocation.count == clients.count) {
                    //res.end('{"success":"false"}');
                    callback(null);
                }
            });
        } catch (e) {
            console.log("error: " + e);
            callback(null);
            //res.end('{"success":"false"}');
        }
    });
}

function sendSMS(cmxUserInfo, user) {
    console.log('sending sms about: ' + JSON.stringify(cmxUserInfo));
    console.log('sending sms to: ' + JSON.stringify(user));

    if(cmxUserInfo != null) twilioclient.sendMessage({

        to: user.telephone, // Any number Twilio can deliver to
        from: '+14154834220', // A number you bought from Twilio and can use for outbound communication
        body: 'Earthquake Alert! The last known location of ' + user.username + ' is here: ' + 'http://maps.googleapis.com/maps/api/staticmap?size=480x480&markers=icon:http://chart.apis.google.com/chart?chst=d_map_pin_icon%26chld=pin%257C996600%7C' + cmxUserInfo.GeoCoordinate[0].$.lattitude + ',' + cmxUserInfo.GeoCoordinate[0].$.longitude + '&sensor=false' // body of the SMS message

    }, function (err, responseData) { //this function is executed when a response is received from Twilio

        if (!err) { // "err" is an error received during the request, if any

            // "responseData" is a JavaScript object containing data received from Twilio.
            // A sample response from sending an SMS message is here (click "JSON" to see how the data appears in JavaScript):
            // http://www.twilio.com/docs/api/rest/sending-sms#example-1

            console.log(responseData.from); // outputs "+14506667788"
            console.log(responseData.body); // outputs "word to your mother."
        }
    });
}

module.exports = router;
