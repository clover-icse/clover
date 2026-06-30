int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;
    

    // loop body
    while(unknown()){
        if((x > 100) ){
            y = y + 1;
        }else if((x % 10 < 5)){
            y = y + 1;
        }else{
            y = y;
            z = z + 1;
        }  
        x = x + 1;    
    }

    // post-condition
    if(x > 100){
        assert(y > z);
    }
    
}