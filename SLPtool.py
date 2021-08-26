# -*- coding: utf-8 -*-
"""
Created on Thu May 27 10:47:10 2021

@author: tongx02
"""

import sleap
import numpy as np
import math
import pandas as pd

def exportCSV(SLPfile,model='2BM'):
    if model=='2BM':
        labels=sleap.load_file(SLPfile)
        CSVname=SLPfile[:-4]+'.csv'
        BPList=['Ear_left','Ear_right','Nose','Implant','Head','Neck','Center','Lateral_left','Lateral_right','Tail_base']
        track0List=list()
        track1List=list()
        data=labels.predicted_instances
        tracks=labels.tracks
        ntracks=len(tracks)
        nframes=data[len(data)-1].frame_idx+1
        trackList,frameList,implantList,headList,frameIndList=getLists(data,tracks,ntracks,nframes)
        sanityFlag=sanityCheck(frameIndList,nframes,labels,data)
        if sanityFlag==-1:
            return
        for iFrame in range(0,nframes):
            tempIndList=frameIndList[iFrame]
            implant=0
            for iIns in range(0,len(tempIndList)):
                if data[frameIndList[iFrame][iIns]].track==labels.tracks[0] or data[frameIndList[iFrame][iIns]].track==labels.tracks[2]:
                    track0List.append(frameIndList[iFrame][iIns])
                    implant=1
            if implant==0:
                track0List.append(None)
            head=0
            for iIns in range(0,len(tempIndList)):
                if data[frameIndList[iFrame][iIns]].track==labels.tracks[1] or data[frameIndList[iFrame][iIns]].track==labels.tracks[3]:
                    track1List.append(frameIndList[iFrame][iIns])
                    head=1
            if head==0:
                track1List.append(None)
        table={}
        df=pd.DataFrame()
        for iBP in BPList:
            table[iBP+'_individual1_x']=list()
            table[iBP+'_individual1_y']=list()
            table[iBP+'_individual1_score']=list()
        for iBP in BPList:
            table[iBP+'_individual2_x']=list()
            table[iBP+'_individual2_y']=list()
            table[iBP+'_individual2_score']=list()
        for iFrame in range(0,nframes):
            if track0List[iFrame]==None:
                for iBP in BPList:
                    table[iBP+'_individual1_x'].append(None)
                    table[iBP+'_individual1_y'].append(None)
                    table[iBP+'_individual1_score'].append(None)
            else:
                ins=track0List[iFrame]
                CurrNodeList=list()
                for k in range(0,len(data[ins].nodes)):
                    CurrNodeList.append(data[ins].nodes[k].name)
                for iBP in BPList:
                    if iBP not in CurrNodeList:
                        table[iBP+'_individual1_x'].append(None)
                        table[iBP+'_individual1_y'].append(None)
                        table[iBP+'_individual1_score'].append(None)
                    else:
                        table[iBP+'_individual1_x'].append(data[ins][iBP].x)
                        table[iBP+'_individual1_y'].append(data[ins][iBP].y)
                        table[iBP+'_individual1_score'].append(data[ins][iBP].score)
            if track1List[iFrame]==None:
                for iBP in BPList:
                    table[iBP+'_individual2_x'].append(None)
                    table[iBP+'_individual2_y'].append(None)
                    table[iBP+'_individual2_score'].append(None)
            else:
                ins=track1List[iFrame]
                CurrNodeList=list()
                for k in range(0,len(data[ins].nodes)):
                    CurrNodeList.append(data[ins].nodes[k].name)
                for iBP in BPList:
                    if iBP not in CurrNodeList:
                        table[iBP+'_individual2_x'].append(None)
                        table[iBP+'_individual2_y'].append(None)
                        table[iBP+'_individual2_score'].append(None)
                    else:
                        table[iBP+'_individual2_x'].append(data[ins][iBP].x)
                        table[iBP+'_individual2_y'].append(data[ins][iBP].y)
                        table[iBP+'_individual2_score'].append(data[ins][iBP].score)
        for iBP in BPList:
            df[iBP+'_individual1_x']=table[iBP+'_individual1_x'][:]
            df[iBP+'_individual1_y']=table[iBP+'_individual1_y'][:]
            df[iBP+'_individual1_score']=table[iBP+'_individual1_score'][:]
        for iBP in BPList:
            df[iBP+'_individual2_x']=table[iBP+'_individual2_x'][:]
            df[iBP+'_individual2_y']=table[iBP+'_individual2_y'][:]
            df[iBP+'_individual2_score']=table[iBP+'_individual2_score'][:]
        df.to_csv(CSVname)
    elif model=='BW':
        labels=sleap.load_file(SLPfile)
        CSVname=SLPfile[:-4]+'.csv'
        BPListPrecursor=['Ear_left','Ear_right','Nose','Implant','Head','Neck','Center','Lateral_left','Lateral_right','Tail_base']
        BPList=list()
        for i in range(0,2):
            for iBP in range(0,len(BPListPrecursor)):
                BPList.append(BPListPrecursor[iBP]+'_'+str(i+1))
        data=labels.predicted_instances
        nframes=data[len(data)-1].frame_idx+1
        table={}
        df=pd.DataFrame()
        for iBP in BPList:
            table[iBP+'_x']=list()
            table[iBP+'_y']=list()
            table[iBP+'_score']=list()
        for iFrame in range(0,nframes):
            ins=iFrame
            CurrNodeList=list()
            for k in range(0,len(data[ins].nodes)):
                CurrNodeList.append(data[ins].nodes[k].name)
            for iBP in BPList:
                if iBP not in CurrNodeList:
                    table[iBP+'_x'].append(None)
                    table[iBP+'_y'].append(None)
                    table[iBP+'_score'].append(None)
                else:
                    table[iBP+'_x'].append(data[ins][iBP].x)
                    table[iBP+'_y'].append(data[ins][iBP].y)
                    table[iBP+'_score'].append(data[ins][iBP].score)
        for iBP in BPList:
            df[iBP+'_x']=table[iBP+'_x'][:]
            df[iBP+'_y']=table[iBP+'_y'][:]
            df[iBP+'_score']=table[iBP+'_score'][:]
        df.to_csv(CSVname)
    else:
        print('Please enter a valid model name (2BM or BW)!')
            
    

def fixIDswap(SLPfile):
    windowLength=5#should be an odd number for symmetry
    reliableThres=0.6
    moveThres=50
    labels=sleap.load_file(SLPfile)
    #labels.tracks=labels.tracks[0:2]
    SLPfile_new=SLPfile[:-4]+'_fixed.slp'
    data=labels.predicted_instances
    tracks=labels.tracks
    ntracks=len(tracks)
    nframes=data[len(data)-1].frame_idx+1
    trackList,frameList,implantList,headList,frameIndList=getLists(data,tracks,ntracks,nframes)
    #tracklist is a list array with elements of each elementary list representing data indices of each track
    #framelist is a list array with elements of each elementary list representing track indices in each frame
    #headlist and implantlist are lists withsize of len(data). Each element represents score of head/implant of a data point
    data,track0List,track1List,reliableFrameList=initializeTracks(windowLength,nframes,trackList,frameList,headList,implantList,tracks,data,reliableThres,labels)
    unreliableList=createUnreliableList(track0List,track1List,data)
    for i in unreliableList:
        data[i].track=labels.tracks[4]
    #    data=refineTracks(nframes,frameIndList,unreliableList,track0List,track1List,data,labels)
    track0ListNew,track1ListNew,data=propogateTracks(reliableFrameList,frameIndList,track0List,track1List,tracks,nframes,labels,data,moveThres)
    track2ListNew,track3ListNew,labels,data=finalizeTracks(reliableFrameList,track0ListNew,track1ListNew,frameIndList,nframes,tracks,labels,data,moveThres)
    SanityFlag=sanityCheck(frameIndList,nframes,labels,data)
    labels.save(SLPfile_new)

def backLoosePropagate(reliableFrameList,frameIndList,track0ListNew,track1ListNew,track2ListNew,track3ListNew,nframes,labels,data,moveThres):
    startF=reliableFrameList[-1]
    for i in range(nframes-startF,nframes):
        iFrame=nframes-i-1
        if (track0ListNew[iFrame]!=None or track2ListNew[iFrame]!=None) and (track1ListNew[iFrame]!=None or track3ListNew[iFrame]!=None):
            pass
        else:
            if track0ListNew[iFrame+1]!=None:
                implantNext=track0ListNew[iFrame+1]
            else:
                implantNext=track2ListNew[iFrame+1]
            if track1ListNew[iFrame+1]!=None:
                headNext=track1ListNew[iFrame+1]
            else:
                headNext=track3ListNew[iFrame+1]
            implantCandidates,headCandidates=getLooseCandidates(frameIndList,implantNext,headNext,iFrame,data,moveThres)
            if len(implantCandidates)==1 and implantCandidates[0]!=None and len(headCandidates)==1 and implantCandidates[0]==headCandidates[0]:
               if looseCheckMove(implantNext,implantCandidates[0],data)<looseCheckMove(headNext,headCandidates[0],data):
                   if track0ListNew[iFrame]==None and track2ListNew[iFrame]==None:
                       track2ListNew[iFrame]=implantCandidates[0]
                       data[implantCandidates[0]].track=labels.tracks[0]
               else:
                   if track1ListNew[iFrame]==None and track3ListNew[iFrame]==None:
                       track3ListNew[iFrame]=headCandidates[0]
                       data[headCandidates[0]].track=labels.tracks[1]
            else:
                if len(implantCandidates)>1 and len(headCandidates)>1:
                    minVal=moveThres+1
                    for iIns0 in range(0,len(implantCandidates)):
                        if looseCheckMove(implantNext,implantCandidates[iIns0],data)<minVal:
                            minVal=looseCheckMove(implantNext,implantCandidates[iIns0],data)
                            implantCandidate=implantCandidates[iIns0]
                    minVal=moveThres+1
                    for iIns1 in range(0,len(headCandidates)):
                        if looseCheckMove(headNext,headCandidates[iIns1],data)<minVal:
                            minVal=looseCheckMove(headNext,headCandidates[iIns1],data)
                            headCandidate=headCandidates[iIns1]
                    if implantCandidate!=headCandidate:
                        if track0ListNew[iFrame]==None and track2ListNew[iFrame]==None:
                            track2ListNew[iFrame]=implantCandidate
                            data[implantCandidate].track=labels.tracks[0]
                        if track1ListNew[iFrame]==None and track3ListNew[iFrame]==None:
                            track3ListNew[iFrame]=headCandidate
                            data[headCandidate].track=labels.tracks[1]
                else:
                    if len(implantCandidates)==1 and implantCandidates[0]!=None:
                        if track0ListNew[iFrame]==None and track2ListNew[iFrame]==None:
                            track2ListNew[iFrame]=implantCandidates[0]
                            data[implantCandidates[0]].track=labels.tracks[0]
                    if len(headCandidates)==1 and headCandidates[0]!=None:
                        if track1ListNew[iFrame]==None and track3ListNew[iFrame]==None:
                            track3ListNew[iFrame]=headCandidates[0]
                            data[headCandidates[0]].track=labels.tracks[1]
    return track0ListNew,track1ListNew,data
    
def backPropagate(reliableFrameList,frameIndList,track0ListNew,track1ListNew,nframes,labels,data,moveThres):
    startF=reliableFrameList[-1]
    for i in range(nframes-startF,nframes):
        iFrame=nframes-i-1
        if track0ListNew[iFrame]!=None and track1ListNew[iFrame]!=None:
            pass
        else:
            implantCandidates,headCandidates=getCandidates(frameIndList,track0ListNew[iFrame+1],track1ListNew[iFrame+1],iFrame,data,moveThres)
            if len(implantCandidates)==1 and implantCandidates[0]!=None and len(headCandidates)==1 and implantCandidates[0]==headCandidates[0]:
               if checkMove(track0ListNew[iFrame+1],implantCandidates[0],data)<checkMove(track1ListNew[iFrame+1],headCandidates[0],data):
                   if track0ListNew[iFrame]==None:
                       track0ListNew[iFrame]=implantCandidates[0]
                       data[implantCandidates[0]].track=labels.tracks[0]
               else:
                   if track1ListNew[iFrame]==None:
                       track1ListNew[iFrame]=headCandidates[0]
                       data[headCandidates[0]].track=labels.tracks[1]
            else:
                if len(implantCandidates)>1 and len(headCandidates)>1:
                    minVal=moveThres+1
                    for iIns0 in range(0,len(implantCandidates)):
                        if checkMove(track0ListNew[iFrame+1],implantCandidates[iIns0],data)<minVal:
                            minVal=checkMove(track0ListNew[iFrame+1],implantCandidates[iIns0],data)
                            implantCandidate=implantCandidates[iIns0]
                    minVal=moveThres+1
                    for iIns1 in range(0,len(headCandidates)):
                        if checkMove(track1ListNew[iFrame+1],headCandidates[iIns1],data)<minVal:
                            minVal=checkMove(track1ListNew[iFrame+1],headCandidates[iIns1],data)
                            headCandidate=headCandidates[iIns1]
                    if implantCandidate!=headCandidate:
                        if track0ListNew[iFrame]==None:
                            track0ListNew[iFrame]=implantCandidate
                            data[implantCandidate].track=labels.tracks[0]
                        if track1ListNew[iFrame]==None:
                            track1ListNew[iFrame]=headCandidate
                            data[headCandidate].track=labels.tracks[1]
                else:
                    if len(implantCandidates)==1 and implantCandidates[0]!=None:
                        if track0ListNew[iFrame]==None:
                            track0ListNew[iFrame]=implantCandidates[0]
                            data[implantCandidates[0]].track=labels.tracks[0]
                    if len(headCandidates)==1 and headCandidates[0]!=None:
                        if track1ListNew[iFrame]==None:
                            track1ListNew[iFrame]=headCandidates[0]
                            data[headCandidates[0]].track=labels.tracks[1]
    return track0ListNew,track1ListNew,data
            
def checkMove(InsPrev,InsCurr,data):
    PrevNodeList=list()
    CurrNodeList=list()
    for k in range(0,len(data[InsPrev].nodes)):
        PrevNodeList.append(data[InsPrev].nodes[k].name)
    for k in range(0,len(data[InsCurr].nodes)):
        CurrNodeList.append(data[InsCurr].nodes[k].name)
    list1_as_set = set(PrevNodeList)
    intersection = list1_as_set.intersection(CurrNodeList)
    CBPlist = list(intersection)
    dist=0
    for i in range(0,len(CBPlist)):
        dist=dist+math.sqrt((data[InsPrev][CBPlist[i]].x-data[InsCurr][CBPlist[i]].x)**2+(data[InsPrev][CBPlist[i]].y-data[InsCurr][CBPlist[i]].y)**2)
    if len(CBPlist):
        dist=dist/len(CBPlist)
    else:
        dist=9999    
    return dist

def createUnreliableList(track0List,track1List,data):#abandoned
    unreliableList=list()
    for i in range(0,len(data)):
        if i not in track0List and i not in track1List:
            unreliableList.append(i)
    return unreliableList
    
def dataIndFromFrameTrack(iFrame,tracks,trackList,TrackInd,data):
    shift=min(iFrame-tracks[TrackInd].spawned_on,len(trackList[TrackInd])-1)
    while data[trackList[TrackInd][shift]].frame_idx>iFrame:
        shift=shift-1
    return shift    

def finalizeTracks(reliableFrameList,track0ListNew,track1ListNew,frameIndList,nframes,tracks,labels,data,moveThres):
    track0ListNew,track1ListNew,data=backPropagate(reliableFrameList,frameIndList,track0ListNew,track1ListNew,nframes,labels,data,moveThres)
    track2ListNew,track3ListNew,data=loosePropagate(reliableFrameList,frameIndList,track0ListNew,track1ListNew,tracks,nframes,labels,data,moveThres)
    for iFrame in range(0,nframes):
        labels,data=removeDiscardedIns(track0ListNew,track1ListNew,track2ListNew,track3ListNew,frameIndList,iFrame,labels,data)
    return track2ListNew,track3ListNew,labels,data
    
def getAvrHeadScore(windowLength,iFrame,TrackInd,trackList,headList,tracks,nframes,data):
    VIC=(windowLength-1)/2
    shift=min(iFrame-tracks[TrackInd].spawned_on,len(trackList[TrackInd])-1)
    tempHeadList=list()
    while data[trackList[TrackInd][shift]].frame_idx>iFrame:
        shift=shift-1
    VICcount=0
    tempFrame=iFrame
    tempshift=shift
    while VICcount<=VIC and tempFrame>=0 and tempshift>=0 and data[trackList[TrackInd][tempshift]].frame_idx==tempFrame:
        dataInd=trackList[TrackInd][tempshift]
        tempHeadList.append(headList[dataInd])
        VICcount=VICcount+1
        tempFrame=tempFrame-1
        tempshift=tempshift-1
    VICcount=1
    tempFrame=iFrame+1
    tempshift=shift+1
    while VICcount<=VIC and tempFrame<nframes and tempshift<len(trackList[TrackInd]) and trackList[TrackInd][tempshift]==tempFrame:
        dataInd=trackList[TrackInd][tempshift]
        tempHeadList.append(headList[dataInd])
        VICcount=VICcount+1
        tempFrame=tempFrame+1
        tempshift=tempshift+1
    avrHeadScore=np.mean(tempHeadList)
    return avrHeadScore

def getAvrImplantScore(windowLength,iFrame,TrackInd,trackList,implantList,tracks,nframes,data):
    VIC=(windowLength-1)/2
    shift=min(iFrame-tracks[TrackInd].spawned_on,len(trackList[TrackInd])-1)
    tempImplantList=list()
    while data[trackList[TrackInd][shift]].frame_idx>iFrame:
        shift=shift-1
    VICcount=0
    tempFrame=iFrame
    tempshift=shift
    while VICcount<=VIC and tempFrame>=0 and tempshift>=0 and data[trackList[TrackInd][tempshift]].frame_idx==tempFrame:
        dataInd=trackList[TrackInd][tempshift]
        tempImplantList.append(implantList[dataInd])
        VICcount=VICcount+1
        tempFrame=tempFrame-1
        tempshift=tempshift-1
    VICcount=1
    tempFrame=iFrame+1
    tempshift=shift+1
    while VICcount<=VIC and tempFrame<nframes and tempshift<len(trackList[TrackInd]) and trackList[TrackInd][tempshift]==tempFrame:
        dataInd=trackList[TrackInd][tempshift]
        tempImplantList.append(implantList[dataInd])
        VICcount=VICcount+1
        tempFrame=tempFrame+1
        tempshift=tempshift+1
    avrImplantScore=np.mean(tempImplantList)
    return avrImplantScore

def getCandidates(frameIndList,InsPrevImplant,InsPrevHead,iFrame,data,moveThres):
    implantCandidates=list()
    headCandidates=list()
    if InsPrevImplant==None:
        implantCandidates.append(None)
    if InsPrevHead==None:
        headCandidates.append(None)
    for iIns in range(0,len(frameIndList[iFrame])):
        if InsPrevImplant!=None:
            dist0=checkMove(InsPrevImplant,frameIndList[iFrame][iIns],data)
            if dist0<moveThres:
                implantCandidates.append(frameIndList[iFrame][iIns])
        if InsPrevHead!=None:
            dist1=checkMove(InsPrevHead,frameIndList[iFrame][iIns],data)
            if dist1<moveThres:
                headCandidates.append(frameIndList[iFrame][iIns])
    return implantCandidates,headCandidates

def getLists(data,tracks,ntracks,nframes):
    trackList=list()
    frameList=list()
    frameIndList=list()
    implantList=list()
    headList=list()
    for i in range(0,ntracks):
        trackList.append(list())      
    for i in range(0,nframes):
        frameList.append(list()) 
        frameIndList.append(list())
    for i in range(0,len(data)):#retrieve each track
        trackInd=tracks.index(data[i].track)
        frameInd=data[i].frame_idx
        trackList[trackInd].append(i)
        frameList[frameInd].append(trackInd)
        frameIndList[frameInd].append(i)
        tempNodeList=list()
        for k in range(0,len(data[i].nodes)):
            tempNodeList.append(data[i].nodes[k].name)
        try:
            headInd=tempNodeList.index('Head')
            headList.append(data[i].points[headInd].score)
        except ValueError:
            headInd=-1
            headList.append(0)
        try:
            implantInd=tempNodeList.index('Implant')
            implantList.append(data[i].points[implantInd].score)
        except ValueError:
            implantInd=-1
            implantList.append(0)
    return trackList,frameList,implantList,headList,frameIndList

def getLooseCandidates(frameIndList,InsPrevImplant,InsPrevHead,iFrame,data,moveThres):
    implantCandidates=list()
    headCandidates=list()
    if InsPrevImplant==None:
        implantCandidates.append(None)
    if InsPrevHead==None:
        headCandidates.append(None)
    for iIns in range(0,len(frameIndList[iFrame])):
        if InsPrevImplant!=None:
            dist0=looseCheckMove(InsPrevImplant,frameIndList[iFrame][iIns],data)
            if dist0<moveThres:
                implantCandidates.append(frameIndList[iFrame][iIns])
        if InsPrevHead!=None:
            dist1=looseCheckMove(InsPrevHead,frameIndList[iFrame][iIns],data)
            if dist1<moveThres:
                headCandidates.append(frameIndList[iFrame][iIns])
    return implantCandidates,headCandidates 

def initializeTracks(windowLength,nframes,trackList,frameList,headList,implantList,tracks,data,reliableThres,labels):
    track0List=list()#implanted mouse
    track1List=list()#non-implantd mouse
    reliableFrameList=list()
    for iFrame in range(0,nframes):
        tempHeadScores=list()
        tempImplantScores=list()
        for iTrack in range(0,len(frameList[iFrame])):#iterate tracks in frame i
            TrackInd=frameList[iFrame][iTrack]
            tempHeadScores.append(getAvrHeadScore(windowLength,iFrame,TrackInd,trackList,headList,tracks,nframes,data))
            tempImplantScores.append(getAvrImplantScore(windowLength,iFrame,TrackInd,trackList,implantList,tracks,nframes,data))
        highImplant=0
        highHead=0
        for iTrack in range(0,len(tempHeadScores)):
            if tempHeadScores[iTrack]>=reliableThres:
                highHead=highHead+1
            if tempImplantScores[iTrack]>=reliableThres:
                highImplant=highImplant+1
        if highImplant==1 and highHead==1:
            for iTrack in range(0,len(tempHeadScores)):
                if tempImplantScores[iTrack]>=reliableThres:
                    TrackInd=frameList[iFrame][iTrack]
                    shift=dataIndFromFrameTrack(iFrame,tracks,trackList,TrackInd,data)
                    data[trackList[TrackInd][shift]].track=labels.tracks[0]
                    track0List.append(trackList[TrackInd][shift])
            for iTrack in range(0,len(tempHeadScores)):
                if tempHeadScores[iTrack]>=reliableThres:
                    TrackInd=frameList[iFrame][iTrack]
                    shift=dataIndFromFrameTrack(iFrame,tracks,trackList,TrackInd,data)
                    data[trackList[TrackInd][shift]].track=labels.tracks[1]
                    track1List.append(trackList[TrackInd][shift])
            if track0List[-1]==track1List[-1]:
                track0List.remove(track0List[-1])
                track1List.remove(track1List[-1])
            else:
                reliableFrameList.append(iFrame)
    return data,track0List,track1List,reliableFrameList

def looseCheckMove(InsPrev,InsCurr,data):
    PrevNodeList=list()
    CurrNodeList=list()
    prevXList=list()
    prevYList=list()
    currXList=list()
    currYList=list()
    for k in range(0,len(data[InsPrev].nodes)):
        PrevNodeList.append(data[InsPrev].nodes[k].name)
    for k in range(0,len(data[InsCurr].nodes)):
        CurrNodeList.append(data[InsCurr].nodes[k].name)
    for iPrev in range(0,len(PrevNodeList)):
        prevXList.append(data[InsPrev][PrevNodeList[iPrev]].x)
        prevYList.append(data[InsPrev][PrevNodeList[iPrev]].y)
    for iCurr in range(0,len(CurrNodeList)):
        currXList.append(data[InsCurr][CurrNodeList[iCurr]].x)
        currYList.append(data[InsCurr][CurrNodeList[iCurr]].y)
    medianPrev_x=np.median(prevXList)
    medianPrev_y=np.median(prevYList)
    medianCurr_x=np.median(currXList)
    medianCurr_y=np.median(currYList)
    dist=math.sqrt((medianPrev_x-medianCurr_x)**2+(medianPrev_y-medianCurr_y)**2)
    return dist

def loosePropagate(reliableFrameList,frameIndList,track0ListNew,track1ListNew,tracks,nframes,labels,data,moveThres):
    track2ListNew=list()
    track3ListNew=list()
    startF=reliableFrameList[0]
    for i in range(0,nframes):
        track2ListNew.append(None)
        track3ListNew.append(None)
    iFrame=startF
    while iFrame<nframes:
        if track0ListNew[iFrame]==None or track1ListNew[iFrame]==None:
            if track0ListNew[iFrame-1]!=None:
                implantPrev=track0ListNew[iFrame-1]
            else:
                implantPrev=track2ListNew[iFrame-1]
            if track1ListNew[iFrame-1]!=None:
                headPrev=track1ListNew[iFrame-1]
            else:
                headPrev=track3ListNew[iFrame-1]
            implantCandidates,headCandidates=getLooseCandidates(frameIndList,implantPrev,headPrev,iFrame,data,moveThres)
            if len(implantCandidates)==1 and implantCandidates[0]!=None and len(headCandidates)==1 and implantCandidates[0]==headCandidates[0]:
               if looseCheckMove(implantPrev,implantCandidates[0],data)<looseCheckMove(headPrev,headCandidates[0],data):
                   track2ListNew[iFrame]=implantCandidates[0]
                   data[implantCandidates[0]].track=labels.tracks[0]
               else:
                   track3ListNew[iFrame]=headCandidates[0]
                   data[headCandidates[0]].track=labels.tracks[1]
            else:
                if len(implantCandidates)>1 and len(headCandidates)>1:
                    minVal=moveThres+1
                    for iIns0 in range(0,len(implantCandidates)):
                        if looseCheckMove(implantPrev,implantCandidates[iIns0],data)<minVal:
                            minVal=looseCheckMove(implantPrev,implantCandidates[iIns0],data)
                            implantCandidate=implantCandidates[iIns0]
                    minVal=moveThres+1
                    for iIns1 in range(0,len(headCandidates)):
                        if looseCheckMove(headPrev,headCandidates[iIns1],data)<minVal:
                            minVal=looseCheckMove(headPrev,headCandidates[iIns1],data)
                            headCandidate=headCandidates[iIns1]
                    if implantCandidate!=headCandidate:
                        track2ListNew[iFrame]=implantCandidate
                        data[implantCandidate].track=labels.tracks[0]
                        track3ListNew[iFrame]=headCandidate
                        data[headCandidate].track=labels.tracks[1]
                else:
                    if len(implantCandidates)==1 and implantCandidates[0]!=None:
                        track2ListNew[iFrame]=implantCandidates[0]
                        data[implantCandidates[0]].track=labels.tracks[0]
                    if len(headCandidates)==1 and headCandidates[0]!=None:
                        track3ListNew[iFrame]=headCandidates[0]
                        data[headCandidates[0]].track=labels.tracks[1]
                    common=0
                    if len(implantCandidates)>1:
                        for iIns1 in range(0,len(headCandidates)):
                            if headCandidates[iIns1] in implantCandidates:
                                common=1
                        if common==0:
                            minVal=moveThres+1
                            for iIns0 in range(0,len(implantCandidates)):
                                if looseCheckMove(implantPrev,implantCandidates[iIns0],data)<minVal:
                                    minVal=looseCheckMove(implantPrev,implantCandidates[iIns0],data)
                                    implantCandidate=implantCandidates[iIns0]
                            if track0ListNew[iFrame]==None and track2ListNew[iFrame]==None:
                                track2ListNew[iFrame]=implantCandidate
                                data[implantCandidate].track=labels.tracks[2]
                    common=0
                    if len(headCandidates)>1:
                        for iIns0 in range(0,len(implantCandidates)):
                            if implantCandidates[iIns0] in headCandidates:
                                common=1
                        if common==0:
                            minVal=moveThres+1
                            for iIns1 in range(0,len(headCandidates)):
                                if looseCheckMove(headPrev,headCandidates[iIns1],data)<minVal:
                                    minVal=looseCheckMove(headPrev,headCandidates[iIns1],data)
                                    headCandidate=headCandidates[iIns1]
                            if track1ListNew[iFrame]==None and track3ListNew[iFrame]==None:
                                track3ListNew[iFrame]=headCandidate
                                data[headCandidate].track=labels.tracks[3]
            if len(frameIndList[iFrame-1])==1 and len(frameIndList[iFrame])==2:
                if (track0ListNew[iFrame]!=None or track2ListNew[iFrame]!=None) and (track1ListNew[iFrame]==None and track3ListNew[iFrame]==None):
                    if track0ListNew[iFrame]!=None:
                        existingIns=track0ListNew[iFrame]
                    else:
                        existingIns=track2ListNew[iFrame]
                    tempIndList=frameIndList[iFrame]
                    tempIndList.remove(existingIns)
                    tempIns=tempIndList[0]
                    track3ListNew[iFrame]=tempIns
                    data[tempIns].track=labels.tracks[3]
                if (track1ListNew[iFrame]!=None or track3ListNew[iFrame]!=None) and (track0ListNew[iFrame]==None and track2ListNew[iFrame]==None):
                    if track1ListNew[iFrame]!=None:
                        existingIns=track1ListNew[iFrame]
                    else:
                        existingIns=track3ListNew[iFrame]
                    tempIndList=frameIndList[iFrame]
                    tempIndList.remove(existingIns)
                    tempIns=tempIndList[0]
                    track2ListNew[iFrame]=tempIns
                    data[tempIns].track=labels.tracks[2]
            if len(frameIndList[iFrame])==2 and ((track0ListNew[iFrame]!=None or track2ListNew[iFrame]!=None) + (track1ListNew[iFrame]!=None or track3ListNew[iFrame]!=None))==1:
                if track0ListNew[iFrame]!=None or track2ListNew[iFrame]!=None:
                    tempIndList=frameIndList[iFrame]
                    if track0ListNew[iFrame]!=None:
                        existingIns=track0ListNew[iFrame]
                    else:
                        existingIns=track2ListNew[iFrame]
                    tempIndList.remove(existingIns)
                    tempIns=tempIndList[0]
                    track3ListNew[iFrame]=tempIns
                    data[tempIns].track=labels.tracks[3]
                else:
                    tempIndList=frameIndList[iFrame]
                    if track1ListNew[iFrame]!=None:
                        existingIns=track1ListNew[iFrame]
                    else:
                        existingIns=track3ListNew[iFrame]
                    tempIndList.remove(existingIns)
                    tempIns=tempIndList[0]
                    track2ListNew[iFrame]=tempIns
                    data[tempIns].track=labels.tracks[2]
        iFrame=iFrame+1
    return track2ListNew,track3ListNew,data       

def propogateTracks(reliableFrameList,frameIndList,track0List,track1List,tracks,nframes,labels,data,moveThres):
    track0ListNew=list()
    track1ListNew=list()
    startF=reliableFrameList[0]
    for i in range(0,startF):
        track0ListNew.append(None)
        track1ListNew.append(None)
    iFrame=startF
    reliableInd=0
    while iFrame<nframes:
        if iFrame in reliableFrameList:
            track0ListNew.append(track0List[reliableInd])
            track1ListNew.append(track1List[reliableInd])
            reliableInd=reliableInd+1
        else:
            implantCandidates,headCandidates=getCandidates(frameIndList,track0ListNew[iFrame-1],track1ListNew[iFrame-1],iFrame,data,moveThres)
            if len(implantCandidates)==1 and implantCandidates[0]!=None and len(headCandidates)==1 and implantCandidates[0]==headCandidates[0]:
               if checkMove(track0ListNew[iFrame-1],implantCandidates[0],data)<checkMove(track1ListNew[iFrame-1],headCandidates[0],data):
                   track0ListNew.append(implantCandidates[0])
                   data[implantCandidates[0]].track=labels.tracks[0]
                   track1ListNew.append(None)
               else:
                   track1ListNew.append(headCandidates[0])
                   data[headCandidates[0]].track=labels.tracks[1]
                   track0ListNew.append(None)
            else:
                if len(implantCandidates)>1 and len(headCandidates)>1:
                    minVal=moveThres+1
                    for iIns0 in range(0,len(implantCandidates)):
                        if checkMove(track0ListNew[iFrame-1],implantCandidates[iIns0],data)<minVal:
                            minVal=checkMove(track0ListNew[iFrame-1],implantCandidates[iIns0],data)
                            implantCandidate=implantCandidates[iIns0]
                    minVal=moveThres+1
                    for iIns1 in range(0,len(headCandidates)):
                        if checkMove(track1ListNew[iFrame-1],headCandidates[iIns1],data)<minVal:
                            minVal=checkMove(track1ListNew[iFrame-1],headCandidates[iIns1],data)
                            headCandidate=headCandidates[iIns1]
                    if implantCandidate!=headCandidate:
                        track0ListNew.append(implantCandidate)
                        data[implantCandidate].track=labels.tracks[0]
                        track1ListNew.append(headCandidate)
                        data[headCandidate].track=labels.tracks[1]
                    else:
                        track0ListNew.append(None)
                        track1ListNew.append(None)
                else:
                    if len(implantCandidates)==1 and implantCandidates[0]!=None:
                        track0ListNew.append(implantCandidates[0])
                        data[implantCandidates[0]].track=labels.tracks[0]
                    else:
                        track0ListNew.append(None)
        #                data[implantCandidates[0]].track=labels.tracks[2]
                    if len(headCandidates)==1 and headCandidates[0]!=None:
                        track1ListNew.append(headCandidates[0])
                        data[headCandidates[0]].track=labels.tracks[1]
                    else:
                        track1ListNew.append(None)
#                data[headCandidates[0]].track=labels.tracks[2]
            #implantInd,headInd,unreliableFlag=assignIdentities()
        iFrame=iFrame+1
    return track0ListNew,track1ListNew,data
    
def removeDiscardedIns(track0ListNew,track1ListNew,track2ListNew,track3ListNew,frameIndList,iFrame,labels,data):
#    if (track0ListNew[iFrame]!=None or track2ListNew[iFrame]!=None) and (track1ListNew[iFrame]!=None or track3ListNew[iFrame]!=None):
#        resList=list()
#        tempIndList=frameIndList[iFrame]
#        for i in range(0,len(tempIndList)):
#            if track0ListNew[iFrame]==tempIndList[i] or track1ListNew[iFrame]==tempIndList[i] or track2ListNew[iFrame]==tempIndList[i] or track3ListNew[iFrame]==tempIndList[i]:
#                resList.append(i)
#        if len(resList)==0:
#            labels.labeled_frames[iFrame].instances=[]
#        if len(resList)==1:
#            labels.labeled_frames[iFrame].instances=[labels.labeled_frames[iFrame].instances[resList[0]]]
#        if len(resList)==2:
#            labels.labeled_frames[iFrame].instances=[labels.labeled_frames[iFrame].instances[resList[0]],labels.labeled_frames[iFrame].instances[resList[1]]]
    count=0
    for iIns in range(0,len(frameIndList[iFrame])):
        if data[frameIndList[iFrame][iIns]].track==labels.tracks[4]:
            labels.labeled_frames[iFrame].instances.remove(labels.labeled_frames[iFrame].instances[iIns-count])
            count=count+1
    return labels,data

def sanityCheck(frameIndList,nframes,labels,data):
    for iFrame in range(0,nframes):
        count0=0
        count1=1
        for iIns in range(0,len(frameIndList[iFrame])):
            if data[frameIndList[iFrame][iIns]].track==labels.tracks[0] or data[frameIndList[iFrame][iIns]].track==labels.tracks[2]:
                count0=count0=+1
            if data[frameIndList[iFrame][iIns]].track==labels.tracks[1] or data[frameIndList[iFrame][iIns]].track==labels.tracks[3]:
                count1=count1=+1
        if count0>1 or count1>1:
            errmsg='Error: frame ' + str(iFrame) + 'has more than one instance of the same track'
            print(errmsg)
            return -1
    return 0

#def refineTracks(nframes,frameIndList,unreliableList,track0List,track1List,data,labels):
#    for iFrame in range(0,nframes):
#        need=0
#        for iIns in range(0,len(frameIndList[iFrame])):
#            if frameIndList[iFrame][iIns] in unreliableList:
#                need=1
#                break
#        if need:
#            implant=0
#            head=0
#            for iIns in range(0,len(frameIndList[iFrame])):
#                if frameIndList[iFrame][iIns] in track0List:#implanted mouse is determined
#                    implant=1
#                    tempImplantInd=frameIndList[iFrame][iIns]
#                    break
#            for iIns in range(0,len(frameIndList[iFrame])):
#                if frameIndList[iFrame][iIns] in track1List:#non-implanted mouse is determined
#                    head=1
#                    tempHeadInd=frameIndList[iFrame][iIns]
#                    break
#            if implant:
#                try:
#                    tempCandidates=frameIndList[iFrame].remove(tempImplantInd)
#                    if len(tempCandidates)==1:
#                        data[tempCandidates].track=labels.tracks[1]
#                except TypeError or ValueError:
#                    pass
#            if head:
#                try:
#                    tempCandidates=frameIndList[iFrame].remove(tempHeadInd)
#                    if len(tempCandidates)==1:
#                        data[tempCandidates].track=labels.tracks[0]
#                except TypeError or ValueError:
#                    pass
#            if not implant and not head:
#                pass
#    return data