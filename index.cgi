#!/usr/bin/ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'cgi'

@randomwikihow = "http://www.wikihow.com/Special:Randomizer"
@stepcount = rand(4) + 4

class Step 
  attr_reader :stepnum, :step, :position
  attr_writer :position
  def initialize(stepnum, step, position)
  	@stepnum = stepnum
  	@step = step
  	@position = position
  end
end

def getrandomtitle()
	page = Nokogiri::HTML(open(@randomwikihow))
	title = page.css('title').text
	title = title.sub(/ - wikiHow/, "")
	title = title.sub(/ \(with Pictures\)/, "")
	title = title.sub(/ \(with Examples\)/, "")
	title = title.sub(/\: \d* Steps/, "")
	title = title.sub(/^\d* Ways to/, "How to")
	title = title.sub(/^\d* Easy Ways to/, "How to")
	return title
end

def getrandomstep(position)

	page = Nokogiri::HTML(open(@randomwikihow))

	steps = []

	# gather steps from li elements
	lis = page.css('li')

	lis.each  do |li|
	  stepnum = li.css('div.step_num').text
	  if stepnum != ''
	  	stepnum = stepnum.to_i
	    step = li.css('b.whb').text
	    position = :middle
	    if stepnum == 1 
	    	position = :first
	    	if steps.count > 0
		    	steps[-1].position = :last 
		    end
	    end
	    steps << Step.new(stepnum, step, position)
	  end
	end

	steps[-1].position = :last

	positionsteps = steps.find_all {|s| s.position == position}

	return positionsteps[rand(positionsteps.count)].step
end

title = getrandomtitle()

s = "<html><head><title>" + title + "</title>" 
s = s + "<link href='nonsequitur.css' rel='stylesheet'><meta name='viewport' content='width=device-width, initial-scale=1.0, minimum-scale=1.0'>"
s = s + "<body><h2>WikiHow Non Sequitur</h2><h1>" + title + "</h1><ol>"

s = s + "<li>" + getrandomstep(:first) + "</li>"
(2..@stepcount).each do |n|
  s = s + "<li>" + getrandomstep(:middle) + "</li>"
end
s = s + "<li>" + getrandomstep(:last) + "</li></ol>"
s = s + "<div id='credit'><a href='https://github.com/pbinkley/wikihow-nonsequitur'>Github</a></div></body></html>"

cgi = CGI::new()
cgi.out("text/html; charset=UTF-8") { s }
