require 'poseidon'

class EventsController < ActionController::Base
  # GET /notes
  # GET /notes.json
  
  def index
    n = 10
    @events = Event.limit(n)
  end

  # GET /notes/1
  # GET /notes/1.json
  def show
  end

  # GET /notes/new
  def new

    @event = Event.new
    random_string = 'hello' + rand(50000).to_s
    @event.type = 'default type ' + random_string
    @event.title = 'default title ' + random_string
    @event.properties = 'default properties ' + random_string
    @event.save

  end

  # GET /notes/1/edit
  def edit
  end

  # POST /notes
  # POST /notes.json
  def create

  end

  # PATCH/PUT /notes/1
  # PATCH/PUT /notes/1.json
  def update

  end

  # DELETE /notes/1
  # DELETE /notes/1.json
  def destroy
  end



  def publish
    event = Hash.new
    random_string = 'hello' + rand(50000).to_s
    event['type'] = 'object'
    event['title'] = 'activity'
    event['properties'] = 'default properties ' + random_string
    if params[:event_thing]
      event = params[:event_thing]
    else
      p 'theres no event'
    end
    messages = []
    messages << Poseidon::MessageToSend.new("topic1", event.to_json)
    kafka_producer.send_messages(messages)
    p 'sent your message'
    @json_event = event.to_json
  end

  def consume
    require 'json'
    @message_values = []
    messages = kafka_consumer.fetch
    messages.each do |m|
      puts m.value
      @message_values << m.value
      # create a new event from the message
      event_hash = JSON.parse(m.value)
      @event = Event.new
      @event.type = event_hash['type']
      @event.title = event_hash['title']
      @event.properties = event_hash['properties']
      @event.save
    end
  end


  def destroy_all
    Event.destroy_all
  end

  def kafka_producer
    PRODUCER
  end
  def kafka_consumer
    CONSUMER
  end

end