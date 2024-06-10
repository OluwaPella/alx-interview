#!/usr/bin/node
const request = require('request');
const API_URL = 'https://swapi-api.hbtn.io/api';

function promisifiedRequest (url) {
  return new Promise((resolve, reject) => {
    request(url, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        resolve({ response, body });
      }
    });
  });
}

async function fetchCharacterNames (filmId) {
  try {
    const { body: filmBody } = await promisifiedRequest(
      `${API_URL}/films/${filmId}/`
    );
    const film = JSON.parse(filmBody);
    const charactersURL = film.characters;

    const characterNames = await Promise.all(
      charactersURL.map(async (url) => {
        const { body: characterBody } = await promisifiedRequest(url);
        const character = JSON.parse(characterBody);
        return character.name;
      })
    );

    return characterNames;
  } catch (error) {
    throw new Error(`Error fetching character names: ${error}`);
  }
}

async function main () {
  try {
    if (process.argv.length > 2) {
      const filmId = process.argv[2];
      const characterNames = await fetchCharacterNames(filmId);
      console.log(characterNames.join('\n'));
    } else {
      console.log('Please provide a film ID.');
    }
  } catch (error) {
    console.error(error);
  }
}

main();