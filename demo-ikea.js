var substringMatcher = function(ikeaProducts) {
  return function findMatches(q, cb) {
    var matches, substringRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    console.log(q)

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(ikeaProducts, function(i, product) {
      if (substrRegex.test(product['description'])) {
        matches.push(product);
      }
    });

    cb(matches);
  };
};

// console.log(ikeaProducts)

const matcher = substringMatcher(ikeaProducts)

$('.search').keydown((q) => {
  if (q.length < 2) {
    return;
  }
  query = q.currentTarget.value;
  console.log(query);
  

  const  cb = (results) => {
    const $resultsDiv = $('.results');
    $resultsDiv.empty()

    results.forEach((result) => {
      $resultsDiv.append($(`<div>${result.title}<img src="${result.images[0]}"/></div>`))
    })
  }

  matcher(query, cb);
})
 