-- This is the main script. The main script is not supposed to be modified,
-- unless there is a very good reason to do it.
-- Without main script,
-- there is no real simulation (child scripts are not called either in that case).
-- A main script marked as "default" (this is the default case) will use the
-- content of following file: system/dltmscpt.txt. This allows your old simulation
-- scenes to be automatically also using newer features, without explicitely coding
-- them. If you modify the main script, it will be marked as "customized", and you
-- won't benefit of that automatic forward compatibility mechanism.

function sysCall_init()
    sim.handleSimulationStart()
    sim.openModule(sim.handle_all)
    sim.handleGraph(sim.handle_all_except_explicit,0)

    handle=sim.getObjectHandle('Food')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food0')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food1')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food2')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[1] = pos[1] + 0.6 end
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food3')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food4')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1       --This checks if the Y-coordinate overlaps with the Robobo Y-coordinate and moves it if it does.
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)

    handle=sim.getObjectHandle('Food5')
    pos=sim.getObjectPosition(handle,-1)
    pos[1]=((math.random() * 2) - 4.1)
    pos[2]=((math.random() * 2) - 0.2)
    if pos[2] > 0.6 and pos[2] < 1.1
        then pos[2] = pos[2] + 0.5 end
    sim.setObjectPosition(handle, -1, pos)


    food_collected=0
    already_eaten = {}
    print("Scene initialized")
end

function sysCall_actuation()
    sim.resumeThreads(sim.scriptthreadresume_default)
    sim.resumeThreads(sim.scriptthreadresume_actuation_first)
    sim.launchThreadedChildScripts()
    sim.handleChildScripts(sim.syscb_actuation)
    sim.resumeThreads(sim.scriptthreadresume_actuation_last)
    sim.handleCustomizationScripts(sim.syscb_actuation)
    sim.handleAddOnScripts(sim.syscb_actuation)
    sim.handleSandboxScript(sim.syscb_actuation)
    sim.handleModule(sim.handle_all,false)
    simHandleJoint(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
    simHandlePath(sim.handle_all_except_explicit,sim.getSimulationTimeStep()) -- DEPRECATED
    sim.handleMechanism(sim.handle_all_except_explicit)
    sim.handleIkGroup(sim.handle_all_except_explicit)
    sim.handleDynamics(sim.getSimulationTimeStep())
    sim.handleMill(sim.handle_all_except_explicit)
end

function sysCall_sensing()
    -- put your sensing code here
    sim.handleSensingStart()
    sim.handleCollision(sim.handle_all_except_explicit)
    sim.handleDistance(sim.handle_all_except_explicit)
    sim.handleProximitySensor(sim.handle_all_except_explicit)
    sim.handleVisionSensor(sim.handle_all_except_explicit)
    sim.resumeThreads(sim.scriptthreadresume_sensing_first)
    sim.handleChildScripts(sim.syscb_sensing)
    sim.resumeThreads(sim.scriptthreadresume_sensing_last)
    sim.handleCustomizationScripts(sim.syscb_sensing)
    sim.handleAddOnScripts(sim.syscb_sensing)
    sim.handleSandboxScript(sim.syscb_sensing)
    sim.handleModule(sim.handle_all,true)
    sim.resumeThreads(sim.scriptthreadresume_allnotyetresumed)
    sim.handleGraph(sim.handle_all_except_explicit,sim.getSimulationTime()+sim.getSimulationTimeStep())
end

function sysCall_cleanup()
    sim.resetMilling(sim.handle_all)
    sim.resetMill(sim.handle_all_except_explicit)
    sim.resetCollision(sim.handle_all_except_explicit)
    sim.resetDistance(sim.handle_all_except_explicit)
    sim.resetProximitySensor(sim.handle_all_except_explicit)
    sim.resetVisionSensor(sim.handle_all_except_explicit)
    sim.closeModule(sim.handle_all)
end

function sysCall_suspend()
    sim.handleChildScripts(sim.syscb_suspend)
    sim.handleCustomizationScripts(sim.syscb_suspend)
    sim.handleAddOnScripts(sim.syscb_suspend)
    sim.handleSandboxScript(sim.syscb_suspend)
end

function sysCall_suspended()
    sim.handleCustomizationScripts(sim.syscb_suspended)
    sim.handleAddOnScripts(sim.syscb_suspended)
    sim.handleSandboxScript(sim.syscb_suspended)
end

function sysCall_resume()
    sim.handleChildScripts(sim.syscb_resume)
    sim.handleCustomizationScripts(sim.syscb_resume)
    sim.handleAddOnScripts(sim.syscb_resume)
    sim.handleSandboxScript(sim.syscb_resume)
end


function collect_food(handle)
        -- This may be called multiple times before the object is actually moved
        -- up. The bag checks to eat it, if it's not already eaten. It's not a rabbit
        if (not already_eaten[handle]) then
            --print(handle)
            already_eaten[handle]=true
            pos = sim.getObjectPosition(handle, -1)
            pos[3] = pos[3] + 1
            sim.setObjectPosition(handle, -1, pos)
            food_collected = food_collected + 1
            print("Collected food " .. food_collected)
        end
end

function sysCall_contactCallback(inData)
    h1 = sim.getObjectName(inData.handle1)
    --h2 = sim.getObjectName(inData.handle2)
    if h1:startswith("Food") then
        --print( h1 .. " -> " .. h2)
        collect_food(inData.handle1)
    end
    --if h2:startswith("Food") then
    --    print( h1 .. " <- " .. h2)
    --end
    return outData
end

-- By default threaded child scripts switch back to the main thread after 2 ms. The main
-- thread switches back to a threaded child script at one of above's "sim.resumeThreads"
-- location

-- You can define additional system calls here:
--[[
function sysCall_beforeCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be copied")
    end
end

function sysCall_afterCopy(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was copied")
    end
end

function sysCall_beforeDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." will be deleted")
    end
    -- inData.allObjects indicates if all objects in the scene will be deleted
end

function sysCall_afterDelete(inData)
    for key,value in pairs(inData.objectHandles) do
        print("Object with handle "..key.." was deleted")
    end
    -- inData.allObjects indicates if all objects in the scene were deleted
end
--]]